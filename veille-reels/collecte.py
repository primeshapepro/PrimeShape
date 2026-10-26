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
    # Les vues habituelles se calculent sur une période deux fois plus longue,
    # sans les reels épinglés (souvent d'anciens succès qui fausseraient la médiane).
    entree_comptes = {
        "resultsLimit": par_compte,
        "skipPinnedPosts": True,
        "onlyPostsNewerThan": f"{limite - timedelta(days=config['jours_max']):%Y-%m-%d}",
    }

    print(f"1. Reels de {len(comptes)} comptes suivis", flush=True)
    bruts = lancer(ACTEUR_REELS, {"username": comptes, **entree_comptes})

    print(f"2. Reels de {len(hashtags)} hashtags", flush=True)
    bruts_hashtags = lancer(ACTEUR_HASHTAGS, {
        "hashtags": hashtags, "resultsType": "reels", "resultsLimit": par_hashtag,
    })

    # Les comptes trouvés par hashtag dont un reel dépasse le seuil, du plus vu au
    # moins vu : on récupère leurs derniers reels pour connaître leurs vues habituelles.
    suivis = {c.lower() for c in comptes}
    meilleur = {}
    for r in bruts_hashtags:
        auteur = r.get("ownerUsername")
        if est_reel(r) and auteur and auteur.lower() not in suivis and vues(r) >= config["vues_min_hashtag"]:
            meilleur[auteur] = max(meilleur.get(auteur, 0), vues(r))
    a_mesurer = sorted(meilleur, key=meilleur.get, reverse=True)[
        : 3 if args.essai else config["comptes_hashtag_max"]]
    if a_mesurer:
        print(f"3. Vues habituelles de {len(a_mesurer)} comptes découverts", flush=True)
        bruts += lancer(ACTEUR_REELS, {"username": a_mesurer, **entree_comptes})

    par_auteur = {}
    for r in bruts:
        if est_reel(r) and r.get("ownerUsername"):
            par_auteur.setdefault(r["ownerUsername"].lower(), {})[r.get("shortCode") or r.get("url")] = r
    medianes = {
        auteur: statistics.median(vues(r) for r in reels.values())
        for auteur, reels in par_auteur.items() if len(reels) >= 5
    }

    # Les reels mis en avant par les hashtags sont souvent plus anciens : on les garde
    # sur une période plus longue, ce sont des formats qui ont fait leurs preuves.
    limite_hashtag = datetime.now(timezone.utc) - timedelta(days=config["jours_max_hashtag"])
    candidats = {}
    for r, par_hashtag_seul in [(r, False) for r in bruts] + [(r, True) for r in bruts_hashtags]:
        auteur = (r.get("ownerUsername") or "").lower()
        d = date_reel(r)
        cle = r.get("shortCode") or r.get("url")
        if not est_reel(r) or not d or not auteur or cle in candidats:
            continue
        if d >= limite:
            source = "compte suivi" if auteur in suivis else "compte découvert"
        elif d >= limite_hashtag and par_hashtag_seul:
            source = "format qui a cartonné"
        else:
            continue
        candidats[cle] = resume(r, medianes.get(auteur), source)

    resultats = sorted(candidats.values(), key=lambda x: (x["score"] or 0, x["vues"]), reverse=True)
    sortie = DOSSIER / "resultats" / f"{datetime.now():%Y-%m-%d}{'-essai' if args.essai else ''}.json"
    sortie.parent.mkdir(exist_ok=True)
    sortie.write_text(json.dumps(resultats, ensure_ascii=False, indent=2))

    recents = [r for r in resultats if r["source"] != "format qui a cartonné"]
    percent = [r for r in recents if (r["score"] or 0) >= config["score_min"]]
    print(f"\n{len(recents)} reels de moins de {config['jours_max']} jours, "
          f"dont {len(percent)} qui percent (×{config['score_min']} ou plus), "
          f"et {len(resultats) - len(recents)} formats qui ont cartonné via les hashtags.")
    print(f"Fichier : {sortie}")


if __name__ == "__main__":
    main()
