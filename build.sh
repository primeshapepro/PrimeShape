#!/bin/sh
# Prépare le dossier publié par Cloudflare Pages : uniquement les fichiers du site,
# sans les notes de travail (PRODUCT.md, DESIGN.md, .claude, .impeccable…).
set -e
rm -rf _site
mkdir _site
cp -r index.html 404.html avis.json robots.txt sitemap.xml _headers \
  favicon.ico favicon.svg apple-touch-icon.png og-image.jpg \
  assets fonts media merci cgu confidentialite mentions-legales _site/
