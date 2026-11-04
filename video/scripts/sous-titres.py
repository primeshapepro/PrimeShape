#!/usr/bin/env python3
"""Transcrit une vidéo avec Whisper et écrit les sous-titres mot à mot pour Remotion.

Usage :
    python3 scripts/sous-titres.py public/rushes/face-cam.mp4
    python3 scripts/sous-titres.py public/rushes/face-cam.mp4 --modele medium --langue fr

Écrit dans public/sous-titres/ :
    <nom>.json  liste de mots au format Caption de @remotion/captions (pour le format FaceCam)
    <nom>.srt   sous-titres classiques (pour Instagram, CapCut, etc.)
    <nom>.txt   texte brut, pour relire et corriger
"""
import argparse
import json
import sys
from pathlib import Path

DOSSIER_SORTIE = Path(__file__).resolve().parent.parent / "public" / "sous-titres"


def horodatage_srt(secondes: float) -> str:
    ms = int(round(secondes * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", type=Path)
    parser.add_argument("--modele", default="small", help="tiny, base, small (défaut), medium, large-v3, turbo")
    parser.add_argument("--langue", default="fr", help="fr (défaut), en… ou auto")
    parser.add_argument("--sortie", type=Path, default=DOSSIER_SORTIE, help="dossier de sortie")
    args = parser.parse_args()

    if not args.video.exists():
        print(f"Fichier introuvable : {args.video}", file=sys.stderr)
        return 1

    import whisper  # import tardif : le chargement de torch prend quelques secondes

    modele = whisper.load_model(args.modele)
    resultat = modele.transcribe(
        str(args.video),
        language=None if args.langue == "auto" else args.langue,
        word_timestamps=True,
        condition_on_previous_text=False,
        fp16=False,
    )

    mots = []
    for segment in resultat["segments"]:
        for mot in segment.get("words", []):
            texte = mot["word"]
            if not texte.strip():
                continue
            debut, fin = float(mot["start"]), float(mot["end"])
            mots.append({
                # Remotion attend un espace devant chaque mot (sauf collage voulu)
                "text": texte if texte.startswith(" ") else " " + texte,
                "startMs": round(debut * 1000),
                "endMs": round(fin * 1000),
                "timestampMs": round((debut + fin) / 2 * 1000),
                "confidence": round(float(mot.get("probability", 0)), 3),
            })

    args.sortie.mkdir(parents=True, exist_ok=True)
    nom = args.video.stem
    (args.sortie / f"{nom}.json").write_text(json.dumps(mots, ensure_ascii=False, indent=1), encoding="utf-8")

    lignes_srt = []
    for i, segment in enumerate(resultat["segments"], start=1):
        lignes_srt += [str(i), f"{horodatage_srt(segment['start'])} --> {horodatage_srt(segment['end'])}",
                       segment["text"].strip(), ""]
    (args.sortie / f"{nom}.srt").write_text("\n".join(lignes_srt), encoding="utf-8")
    (args.sortie / f"{nom}.txt").write_text(resultat["text"].strip() + "\n", encoding="utf-8")

    print(f"Langue : {resultat.get('language')} · {len(mots)} mots")
    print(f"Écrit : {args.sortie / (nom + '.json')} (+ .srt, .txt)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
