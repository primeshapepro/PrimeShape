"""Prépare la sélection de la semaine pour le catalogue (vignettes et fiches).

Étapes, après `collecte.py` et la sélection faite par Claude :

    python3 veille-reels/preparer.py vignettes AAAA-MM-JJ
        lit resultats/selection-AAAA-MM-JJ.json (l'analyse de Claude, une entrée par
        code de reel) et enregistre une vignette 9:16 de chaque reel retenu dans
        resultats/vignettes-AAAA-MM-JJ/<code>.jpg, à envoyer ensuite dans les
        fichiers du catalogue.

    python3 veille-reels/preparer.py fiches AAAA-MM-JJ images.json
        images.json associe chaque code de reel à l'adresse de sa vignette dans le
        catalogue (« /_blob/... »). Écrit une fiche par reel et la fiche de la
        semaine dans resultats/fiches-AAAA-MM-JJ/, prêtes pour la base du catalogue
        (collections « reels » et « semaines »).

Format d'une entrée de la sélection :
    "<code>": {"rang": 1, "pilier": "motivation" | "exercice" | "sante",
               "accroche": "...", "pourquoi": "...", "ta_version": "...",
               "alerte": "..." (facultatif : format à reprendre, contenu à éviter)}
"""

import json
import sys
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

DOSSIER = Path(__file__).resolve().parent / "resultats"
LARGEUR, HAUTEUR = 360, 640


def code(reel):
    return reel["url"].rstrip("/").split("/")[-1]


def charger(jour):
    reels = {code(r): r for r in json.loads((DOSSIER / f"{jour}.json").read_text())}
    selection = json.loads((DOSSIER / f"selection-{jour}.json").read_text())
    absents = [c for c in selection if c not in reels]
    if absents:
        sys.exit(f"Codes absents de la collecte du {jour} : {', '.join(absents)}")
    return reels, selection


def vignettes(jour):
    reels, selection = charger(jour)
    sortie = DOSSIER / f"vignettes-{jour}"
    sortie.mkdir(exist_ok=True)
    for c in selection:
        with urllib.request.urlopen(reels[c]["image"], timeout=60) as reponse:
            image = Image.open(BytesIO(reponse.read())).convert("RGB")
        w, h = image.size
        if w / h > 9 / 16:
            nw = int(h * 9 / 16)
            image = image.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w * 16 / 9)
            image = image.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        image.resize((LARGEUR, HAUTEUR), Image.LANCZOS).save(
            sortie / f"{c}.jpg", "JPEG", quality=78, optimize=True, progressive=True)
        print(sortie / f"{c}.jpg")


def fiches(jour, fichier_images):
    reels, selection = charger(jour)
    images = json.loads(Path(fichier_images).read_text())
    sortie = DOSSIER / f"fiches-{jour}"
    sortie.mkdir(exist_ok=True)
    for c, analyse in selection.items():
        r = reels[c]
        fiche = {
            "semaine": jour, "compte": r["compte"], "url": r["url"], "date": r["date"],
            "vues": r["vues"], "likes": r["likes"], "commentaires": r["commentaires"],
            "score": r["score"], "mediane_compte": r["mediane_compte"],
            "duree": r["duree_s"], "source": r["source"], "image": images.get(c),
            "alerte": None, **analyse,
        }
        (sortie / f"{c}.json").write_text(json.dumps(fiche, ensure_ascii=False))
    print(f"{len(selection)} fiches dans {sortie}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "vignettes":
        vignettes(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "fiches":
        fiches(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
