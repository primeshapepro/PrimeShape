#!/usr/bin/env bash
# Télécharge et décortique un ou plusieurs reels de référence.
#
#   scripts/reference.sh https://www.instagram.com/reel/XXXX/ [autre lien…]
#
# Pour chaque lien, dans refs/<id>/ (dossier ignoré par Git, ces vidéos ne sont pas à toi) :
#   video.mp4    le reel
#   infos.txt    durée, format, nombre de coupes, plan moyen, BPM de la musique
#   planche.jpg  une image par seconde, horodatée : le montage d'un coup d'œil
#   video.txt    ce qui est dit (Whisper), + video.srt / video.json
#
# Téléchargement : yt-dlp d'abord. Si Instagram refuse (sur ton ordi : ajoute
# --cookies-from-browser chrome dans YTDLP_OPTS ; dans le cloud instagram.com est fermé),
# on passe par Apify (variable APIFY_TOKEN sur ton ordi, rien à faire dans le cloud).
set -euo pipefail

ICI="$(cd "$(dirname "$0")/.." && pwd)"
MODELE="${WHISPER_MODELE:-small}"

if [ "$#" -eq 0 ]; then
  sed -n '2,16p' "$0"
  exit 1
fi

telecharger_apify() {
  local id="$1" dossier="$2"
  curl -sS --max-time 300 -X POST \
    "https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?timeout=280${APIFY_TOKEN:+&token=$APIFY_TOKEN}" \
    -H 'Content-Type: application/json' \
    -d "{\"directUrls\":[\"https://www.instagram.com/reel/$id/\"],\"resultsType\":\"posts\",\"resultsLimit\":1}" \
    -o "$dossier/apify.json"
  local lien
  lien="$(python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d[0]["videoUrl"])' "$dossier/apify.json")"
  curl -sS -L --max-time 300 "$lien" -o "$dossier/video.mp4"
  python3 -I -c '
import json, sys
d = json.load(open(sys.argv[1]))[0]
print("Compte : @" + str(d.get("ownerUsername")))
print("Vues : " + str(d.get("videoPlayCount")) + " · likes : " + str(d.get("likesCount")) + " · commentaires : " + str(d.get("commentsCount")))
print("Son : " + str((d.get("musicInfo") or {}).get("song_name")))
print("Légende :")
print(d.get("caption") or "")
' "$dossier/apify.json" > "$dossier/legende.txt" || true
}

for url in "$@"; do
  id="$(printf '%s' "$url" | sed -E 's#.*/(reels?|p|shorts|video)/([^/?]+).*#\2#; s#[^A-Za-z0-9_-]##g')"
  [ -n "$id" ] || id="ref-$(date +%s)"
  dossier="$ICI/refs/$id"
  mkdir -p "$dossier"
  echo "▸ $id"

  if [ ! -s "$dossier/video.mp4" ]; then
    # shellcheck disable=SC2086
    if ! yt-dlp -q --no-warnings ${YTDLP_OPTS:-} -f 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b' \
        --merge-output-format mp4 -o "$dossier/video.mp4" "$url" 2>/dev/null; then
      case "$url" in
        *instagram.com*) echo "  yt-dlp refusé, passage par Apify…"; telecharger_apify "$id" "$dossier" ;;
        *) echo "  Échec du téléchargement : $url" >&2; continue ;;
      esac
    fi
  fi
  video="$dossier/video.mp4"

  duree="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video")"
  format="$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$video")"
  ffmpeg -hide_banner -nostats -i "$video" -vf "select='gt(scene,0.28)',showinfo" -an -f null - 2>&1 \
    | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$dossier/coupes.txt" || true
  coupes="$(wc -l < "$dossier/coupes.txt" | tr -d ' ')"
  bpm="$(cd "$ICI" && timeout 300 npx --no-install hyperframes beats "$video" --json 2>/dev/null \
    | python3 -I -c 'import json,sys; print(json.load(sys.stdin).get("bpm") or "pas de rythme net")' 2>/dev/null || echo "?")"

  # planche contact : 1 image/s (2/s si moins de 10 s, 1 toutes les 1,5 s au-delà de 50 s)
  cadence="$(python3 -I -c "d=float('$duree'); print(2 if d < 10 else (1 if d < 50 else 0.7))")"
  ffmpeg -hide_banner -loglevel error -y -i "$video" \
    -vf "fps=$cadence,scale=216:384,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=8x6:padding=4:color=black" \
    -frames:v 1 -q:v 4 "$dossier/planche.jpg"

  python3 "$ICI/scripts/sous-titres.py" "$video" --modele "$MODELE" --langue auto --sortie "$dossier" > /dev/null 2>&1 \
    || echo "  (transcription impossible : Whisper est-il installé ?)"

  {
    printf 'Durée : %.1f s · format : %s\n' "$duree" "$format"
    printf 'Coupes détectées : %s · plan moyen : %s s\n' "$coupes" \
      "$(python3 -I -c "print(round(float('$duree')/($coupes+1),2))")"
    printf 'Musique : %s BPM\n' "$bpm"
    printf 'Coupes (s) : %s\n' "$(tr '\n' ' ' < "$dossier/coupes.txt")"
    [ -s "$dossier/legende.txt" ] && cat "$dossier/legende.txt"
    true
  } > "$dossier/infos.txt"
  cat "$dossier/infos.txt" | head -4
  echo "  → $dossier"
done
