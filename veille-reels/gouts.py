"""Fait le bilan des choix d'Andy dans le catalogue, pour affiner la sélection.

Exporter d'abord les deux collections du catalogue dans un même dossier
(ArtifactData, action « list » avec out_dir) : reels/<code>.json et
choix/<code>.json. Puis :

    python3 veille-reels/gouts.py <dossier>

Affiche, pour chaque pilier, sujet, format, langue et compte, combien de
reels Andy a gardés (« À monter » ou « Monté ») et écartés, ce qu'il faut
éviter ou privilégier, et les raisons qu'il a écrites.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

DIMENSIONS = ["pilier", "sujet", "format", "langue", "compte"]


def lire(dossier):
    def corps(fichier):
        d = json.loads(fichier.read_text())
        return d["data"] if isinstance(d.get("data"), dict) else d
    return {f.stem: corps(f) for f in sorted(dossier.glob("*.json"))}


def main():
    racine = Path(sys.argv[1])
    reels = lire(racine / "reels")
    choix = lire(racine / "choix") if (racine / "choix").exists() else {}

    comptes = {dim: defaultdict(lambda: {"garde": 0, "ecarte": 0, "sans_avis": 0}) for dim in DIMENSIONS}
    for code, reel in reels.items():
        statut = (choix.get(code) or {}).get("statut")
        cle = "garde" if statut in ("a_monter", "monte") else "ecarte" if statut == "ecarte" else "sans_avis"
        for dim in DIMENSIONS:
            comptes[dim][reel.get(dim) or "?"][cle] += 1

    a_eviter, a_privilegier = [], []
    for dim in DIMENSIONS:
        print(f"\n{dim.upper()}")
        for valeur, n in sorted(comptes[dim].items(), key=lambda kv: (-kv[1]["garde"], kv[1]["ecarte"])):
            print(f"  {valeur:<40} gardés {n['garde']:>2}   écartés {n['ecarte']:>2}   sans avis {n['sans_avis']:>2}")
            # Les piliers sont le contenu d'Andy, et l'anglais comme le français
            # lui vont : on n'écarte jamais un pilier ni une langue entière.
            if dim not in ("pilier", "langue") and n["ecarte"] >= 2 and n["garde"] == 0:
                a_eviter.append(f"{dim} « {valeur} » ({n['ecarte']} écartés)")
            if n["garde"] >= 2:
                a_privilegier.append(f"{dim} « {valeur} » ({n['garde']} gardés)")

    print("\nÀ ÉVITER :", "; ".join(a_eviter) or "rien pour l'instant")
    print("À PRIVILÉGIER :", "; ".join(a_privilegier) or "rien pour l'instant")
    raisons = [(reels[c].get("numero"), reels[c].get("compte"), d["raison"])
               for c, d in choix.items() if d.get("raison") and c in reels]
    print("\nRAISONS ÉCRITES PAR ANDY :")
    for numero, compte, raison in sorted(raisons, key=lambda r: r[0] or 0):
        print(f"  #{numero or 0:03d} @{compte} : {raison}")
    if not raisons:
        print("  aucune pour l'instant")


if __name__ == "__main__":
    main()
