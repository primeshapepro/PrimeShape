---
name: montage-reels
description: Monter, sous-titrer ou analyser un reel PrimeShape avec Remotion, HyperFrames, ffmpeg, Whisper et yt-dlp, selon la trame tirée des reels de référence d'Andy. À utiliser dès qu'Andy envoie des rushes, demande de monter ou sous-titrer une vidéo, ou envoie un lien de reel comme référence.
---

# Montage des reels PrimeShape

1. Lis d'abord `video/TRAME-REELS.md` : références analysées, mood, les trois formats (Routine, FaceCam, Citation) et la couverture.
2. Charge aussi les skills `primeshape-da` (charte « Noir massif ») et `primeshape-instagram` (ton, fin en DM) s'ils sont disponibles.
3. Outils : tout est dans `video/`.
   - Conteneur cloud neuf : vérifie `which yt-dlp whisper ffmpeg`. S'il en manque, `pip install -U yt-dlp openai-whisper`, puis `cd video && npm install`.
   - Remotion : `src/Root.tsx` (compositions), `src/formats/`, `src/components/`, exemples de props dans `props/`. Rushes dans `public/rushes/` (ignorés par Git).
   - Sous-titres : `python3 scripts/sous-titres.py <vidéo>` → `public/sous-titres/<nom>.json`.
   - Nouvelle référence : `scripts/reference.sh <lien>` → `refs/<id>/` (planche, coupes, BPM, transcription). Regarde la planche, puis ajoute la ligne au tableau de la trame.
   - HyperFrames : `video/hyperframes/` pour les cartons animés en HTML (lis son `CLAUDE.md`).
4. Avant de livrer : `npx tsc --noEmit`, rends 2 ou 3 images clés avec `npx remotion still` et regarde-les (zones sûres, lisibilité, image 0), puis le MP4.
5. Ne jamais commiter les rushes, les musiques ni les vidéos de référence téléchargées.
