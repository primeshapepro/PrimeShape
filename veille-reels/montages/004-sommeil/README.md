# #004 · 8 habitudes pour mieux dormir

Version PrimeShape du tableau du sommeil de @thomas__r7 (#004 du catalogue) :
même format « habitude → effet » à enregistrer, contenu et visuels refaits
(charte « Noir massif », rien de la vidéo d'origine). Reel 1080 × 1920, 12 s,
sans son (Andy ajoute la musique dans Instagram). Validé par Andy le 26/11/2026.

- **Vidéo finale :** fichiers du catalogue, `/_blob/c9f40411857ccf6f1ee75043befd9db7`
  (https://claude.ai/artifact/QyyrrDEwYMtQdhEnSLV5wz).
- **Pour la refaire :** `construire.py` écrit la page HyperFrames.

```bash
npm install lucide-static@0.460.0 gsap@3.12.5 hyperframes@0.8.150   # dans un dossier d'outils
python3 veille-reels/montages/004-sommeil/construire.py <outils>/node_modules/lucide-static/icons <projet>/index.html
# <projet>/assets : gsap.min.js, nippo-variable.woff2 (fonts/ du site),
#                   clash-display.woff2 (police du catalogue, /_blob/7263eb725e6d97688e711baf18b5a8e8)
# <projet>/hyperframes.json, package.json, meta.json : ceux d'un projet hyperframes init
HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell \
  npx --prefix <outils> hyperframes render -o sommeil.mp4 -f 30
```

Légende proposée à Andy :

> Une bonne nuit ne commence pas quand tu te couches : elle se prépare dès le matin 🌙
> Laquelle tu appliques déjà ? Dis-le-moi en commentaire 👇
> Enregistre la vidéo pour ce soir.
> #sommeil #hygienedevie #conseilsante #coachsportif #PrimeShape
