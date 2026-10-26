"""Récupère les reels récents de la niche via Apify et calcule leur score de percée.

Usage :
    python3 veille-reels/collecte.py --essai      # petit essai (peu de reels, coût minime)
    python3 veille-reels/collecte.py              # collecte complète de la semaine

La clé Apify est ajoutée par le secret réseau de l'environnement cloud.
Si elle est fournie en variable d'environnement APIFY_TOKEN, elle est utilisée aussi.

Résultat : veille-reels/resultats/AAAA-MM-JJ.json, trié du plus fort score au plus faible.
"""

import argparse
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://api.apify.com/v2"
ACTEUR_REELS = "apify~instagram-reel-scraper"
ACTEUR_HASHTAGS = "apify~instagram-hashtag-scraper"
DOSSIER = Path(__file__).resolve().parent
CONFIG = DOSSIER / "config.json"


def appel(methode, chemin, corps=None, delai=300):
    url = f"{API}{chemin}"
    entetes = {"Content-Type": "application/json"}
    jeton = os.environ.get("APIFY_TOKEN")
    if jeton:
        entetes["Authorization"] = f"Bearer {jeton}"
    donnees = json.dumps(corps).encode() if corps is not None else None
    requete = urllib.request.Request(url, data=donnees, headers=entetes, method=methode)
    try:
        with urllib.request.urlopen(requete, timeout=delai) as reponse:
            return json.load(reponse)
    except urllib.error.HTTPError as erreur:
        detail = erreur.read().decode(errors="replace")[:300]
        sys.exit(f"Apify a refusé {methode} {chemin} ({erreur.code}) : {detail}")


def lancer(acteur, entree):
    """Lance un acteur Apify, attend la fin et renvoie ses résultats."""
    run = appel("POST", f"/acts/{acteur}/runs", entree)["data"]
    print(f"  {acteur} lancé ({run['id']})", flush=True)
    while run["status"] in ("READY", "RUNNING"):
        time.sleep(10)
        run = appel("GET", f"/actor-runs/{run['id']}")["data"]
    if run["status"] != "SUCCEEDED":
        sys.exit(f"  {acteur} a échoué : {run['status']}")
    cout = run.get("usageTotalUsd")
    print(f"  terminé, coût : {cout:.3f} $" if cout is not None else "  terminé", flush=True)
    return appel("GET", f"/datasets/{run['defaultDatasetId']}/items?clean=true&format=json")


def vues(reel):
    return reel.get("videoPlayCount") or reel.get("videoViewCount") or 0


def date_reel(reel):
    try:
        return datetime.fromisoformat(reel["timestamp"].replace("Z", "+00:00"))
    except (KeyError, ValueError, AttributeError):
        return None


def est_reel(reel):
    return reel.get("type") == "Video" or reel.get("productType") == "clips"


def resume(reel, mediane, source):
    musique = reel.get("musicInfo") or {}
    return {
        "url": reel.get("url"),
        "compte": reel.get("ownerUsername"),
        "date": reel.get("timestamp"),
        "vues": vues(reel),
        "likes": reel.get("likesCount"),
        "commentaires": reel.get("commentsCount"),
        "mediane_compte": mediane,
        "score": round(vues(reel) / mediane, 1) if mediane else None,
        "duree_s": reel.get("videoDuration"),
        "legende": (reel.get("caption") or "")[:600],
        "son": musique.get("song_name") or ("son original" if musique.get("uses_original_audio") else None),
        "image": reel.get("displayUrl"),
        "video": reel.get("videoUrl"),
        "transcription": reel.get("transcript"),
        "source": source,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--essai", action="store_true", help="petit essai à coût minime")
    args = parser.parse_args()

    config = json.loads(CONFIG.read_text())
    comptes = config["comptes"]
    hashtags = config["hashtags"]
    par_compte = config["reels_par_compte"]
    par_hashtag = config["reels_par_hashtag"]
    if args.essai:
        comptes, hashtags = comptes[:3], hashtags[:2]
        par_compte, par_hashtag = 12, 10

    limite = datetime.now(timezone.utc) - timedelta(days=config["jours_max"])

    print(f"1. Reels de {len(comptes)} comptes suivis", flush=True)
    bruts = lancer(ACTEUR_REELS, {"username": comptes, "resultsLimit": par_compte})

    print(f"2. Reels de {len(hashtags)} hashtags", flush=True)
    bruts_hashtags = lancer(ACTEUR_HASHTAGS, {
        "hashtags": hashtags, "resultsType": "reels", "resultsLimit": par_hashtag,
    })

    # Les comptes trouvés par hashtag dont un reel dépasse le seuil : on récupère
    # leurs derniers reels pour connaître leurs vues habituelles.
    deja = {c.lower() for c in comptes}
    a_mesurer = sorted({
        r["ownerUsername"] for r in bruts_hashtags
        if est_reel(r) and r.get("ownerUsername") and r["ownerUsername"].lower() not in deja
        and vues(r) >= config["vues_min_hashtag"]
    })[: 3 if args.essai else config["comptes_hashtag_max"]]
    if a_mesurer:
        print(f"3. Vues habituelles de {len(a_mesurer)} comptes découverts", flush=True)
        bruts += lancer(ACTEUR_REELS, {"username": a_mesurer, "resultsLimit": par_compte})

    par_auteur = {}
    for r in bruts:
        if est_reel(r) and r.get("ownerUsername"):
            par_auteur.setdefault(r["ownerUsername"].lower(), {})[r.get("shortCode") or r.get("url")] = r
    medianes = {
        auteur: statistics.median(vues(r) for r in reels.values())
        for auteur, reels in par_auteur.items() if len(reels) >= 5
    }

    candidats = {}
    sources = [(r, "compte suivi") for r in bruts] + [(r, "hashtag") for r in bruts_hashtags]
    for r, source in sources:
        d = date_reel(r)
        if not est_reel(r) or not d or d < limite or not r.get("ownerUsername"):
            continue
        cle = r.get("shortCode") or r.get("url")
        if cle in candidats:
            continue
        candidats[cle] = resume(r, medianes.get(r["ownerUsername"].lower()), source)

    resultats = sorted(candidats.values(), key=lambda x: (x["score"] or 0, x["vues"]), reverse=True)
    sortie = DOSSIER / "resultats" / f"{datetime.now():%Y-%m-%d}{'-essai' if args.essai else ''}.json"
    sortie.parent.mkdir(exist_ok=True)
    sortie.write_text(json.dumps(resultats, ensure_ascii=False, indent=2))

    percent = [r for r in resultats if (r["score"] or 0) >= config["score_min"]]
    print(f"\n{len(resultats)} reels de moins de {config['jours_max']} jours, "
          f"dont {len(percent)} qui percent (×{config['score_min']} ou plus).")
    print(f"Fichier : {sortie}")


if __name__ == "__main__":
    main()
