# Trame des reels PrimeShape

La règle du jeu pour monter les reels @PrimeShapeFR : ce qu'on a retenu des reels de référence d'Andy, les trois formats qui en sortent, et comment les monter avec les outils du dossier `video/`.

Couleurs, polices et logo : charte « Noir massif » (skill `primeshape-da`, déjà codée dans `src/theme.ts`). Ton et textes : skill `primeshape-instagram` (tutoiement, 30-60 ans débutants, fin en DM).

---

## 1. Les reels de référence

Analysés le 4 novembre 2026 avec `scripts/reference.sh` (planche contact, coupes, transcription Whisper, BPM).

| # | Compte · sujet | Durée | Montage | Texte à l'écran | Son | Ce qu'on prend |
|---|---|---|---|---|---|---|
| 1 | [@trains_gains](https://www.instagram.com/reels/DdH1xg1hi13/) · échauffement jambes | 39 s | Un seul cadre fixe (trépied, pied à tête, salle sombre). 25 coupes sèches, une toutes les 1,5 s : jump cuts dans chaque exercice | Titre minuscule en bas (« LEG DAY WARM-UP ROUTINE » + une ligne en italique), puis le nom de l'exo en minuscules, tout petit, en haut. « 30-45 seconds each for all » | Pas de voix | Même cadre pour tous les exos, texte minuscule : le mouvement parle tout seul |
| 2 | [@abigaildaniellla](https://www.instagram.com/reels/Dcy13BERbGR/) · série « part one » | 46 s | Face cam au micro + plans de coupe lifestyle et captures d'écran. 21 coupes, une toutes les 2,2 s | Sous-titres d'un mot à la fois, au centre. Gros titre « How To Make Engaging Content » à 6 s. Mot-clé « BREAD » à commenter à la fin | Voix face caméra | Accroche « de ça à ça » dès la 1re seconde ; la voix continue sous les plans de coupe ; une seule action demandée à la fin |
| 3 | [@geoff.garlic](https://www.instagram.com/reels/DcsGUDXJaj5/) · « EP 2 », recette racontée | 71 s · 25,6 M vues | Mains en action, plans serrés, une coupe toutes les 3 s | Gros carton de série à 3-7 s (« Cooking a Dish from Every Country · EP 2 »), sous-titres d'un ou deux mots, petits, en bas. Nom du plat en grand à la fin | Voix off + musique douce | Question-accroche (« Which country has the best food? »), une histoire qui avance pendant qu'on voit faire, une chute, des épisodes numérotés |
| 4 | [@victorialvt](https://www.instagram.com/reels/DdxpO19On6A/) · routine pull day | 47 s | Avant/après sur 6 s, puis un plan par exercice (~5,5 s = 3 mesures à 128 BPM), coupes sur le temps | Serif petit et centré : nom de l'exo + « 3 x 10 », parfois une note perso « (my favorite) » | Musique tendance, pas de voix | Coupes calées sur le beat, consigne sous le nom, une petite note perso |
| 5 | [@vision9motion](https://www.instagram.com/reels/DfTRiF0pj_a/) · « Choose your hard » | 8 s | Un seul plan : piste d'athlé la nuit, la personne petite dans le cadre | Une phrase en serif minuscule, en haut | Son original | Format très court qui boucle, image très sombre, une phrase et c'est tout |

## 2. Le mood PrimeShape

- **Sombre et posé.** Salle peu éclairée, extérieur en fin de journée ou de nuit, noirs denses. L'étalonnage `noir` (contraste un peu plus fort, couleurs un peu éteintes) va dans ce sens et colle à la charte Noir massif.
- **Sobre.** Le texte reste petit et rare, sauf l'accroche. Coupes sèches : pas de transitions, pas de zooms, pas d'emojis animés.
- **Vrai.** Caméra fixe, son réel, tenue simple et sombre. Pas de transformation avant/après inventée : un « avant/après » seulement si c'est ton vrai parcours.
- **Notre différence.** Les références parlent à des gens déjà sportifs. Nous, on parle à des 30-60 ans qui débutent ou reprennent : exos simples, consignes claires, ton rassurant, et des sous-titres plus gros que dans les refs (54 px sur pastille noire).

## 3. Les trois formats

### A. Routine (refs 1 et 4) · 25 à 45 s · composition `Routine`

| Temps | À l'écran |
|---|---|
| 0 à 2 s | Accroche par-dessus le 1er plan assombri : label de série + 3 ou 4 lignes, le mot-clé sur aplat vert. La 1re ligne est là dès l'image 0. |
| Ensuite | Un plan fixe par exercice, 4 à 6 s chacun (3 mesures si la musique est vers 120-130 BPM), coupé sec sur le temps. En haut : « EXO 2 / 4 », le nom, la consigne en vert (« 3 × 10 »). Si besoin, 2 ou 3 jump cuts dans le même exo pour montrer une variante. |
| 3 dernières s | Carte de fin : « Tu veux reprendre ? Écris-moi » + l'invitation en DM. |

Tournage : trépied, plan large de la tête aux pieds, caméra à hauteur de hanche, le même cadre pour tous les exos.

### B. Face cam / série (refs 2 et 3) · 30 à 60 s · composition `FaceCam`

| Temps | À l'écran |
|---|---|
| 0 s | Une question ou une promesse dite face caméra : « Tu reprends le sport ? Voilà pourquoi tu lâches au bout de deux jours. » |
| 1 à 4 s | Carton de série par-dessus : « SÉRIE · REPRENDRE LE SPORT · ÉP. 1 ». |
| Corps | Une idée par phrase. Un plan de coupe toutes les 2 à 3 s (toi qui coaches, des gestes, le matériel, la Sainte-Victoire) pendant que ta voix continue. Sous-titres mot à mot (Whisper), mots-clés en vert. |
| Fin | Une phrase de conclusion, puis la carte DM. |

Tournage : micro-cravate ou micro à main, lumière de fenêtre de face, fond rangé. Filme des plans de coupe de 3 à 5 s en plus.

### C. Citation (ref 5) · 6 à 10 s · composition `Citation`

Un plan d'ambiance sombre où tu es petit dans le cadre (échauffement, marche, montée), une phrase courte en haut, `@PRIMESHAPEFR` en pied. Pour que ça boucle bien, le dernier geste rejoint le premier.

## 4. Règles communes

- **Image 0 = vignette du fil.** L'accroche doit déjà se lire à la toute première image.
- **Zones sûres.** Rien d'important dans les 260 px du haut ni dans les 380 px du bas (interface Instagram).
- **Texte.** 28 px minimum. Accroches en Clash Display capitales, tout le reste en Nippo. Le vert reste rare : un seul aplat par écran.
- **Son.** Pour un son tendance Instagram, exporte sans musique et ajoute le son dans l'appli au moment de publier (les sons tendance ne se téléchargent pas). Sinon, mets ta musique dans `public/musique/`.
- **Fin.** Toujours l'invitation en DM, à l'écran et dans la légende.
- **Honnêteté.** Aucun chiffre client, aucun résultat inventé, pas de prix. Les offres sont « à venir ».
- **Couverture.** Composition `Couverture` (image fixe), avec la même accroche que la vidéo.

## 5. Monter un reel, pas à pas

1. Mets tes rushes dans `video/public/rushes/` (et la musique dans `video/public/musique/`).
2. Pour une face cam, lance les sous-titres, puis relis et corrige le `.json` (ou le `.txt`) :
   `python3 scripts/sous-titres.py public/rushes/face-cam.mp4`
3. Copie un exemple de `props/` (`exemple-routine.json`, `exemple-facecam.json`, `exemple-citation.json`, `exemple-couverture.json`) et remplis-le : chemins des rushes, temps en secondes, textes.
4. Aperçu en direct : `npm run studio` (dans `video/`).
5. Rendu : `npx remotion render FaceCam out/mon-reel.mp4 --props=props/mon-reel.json`
6. Couverture : `npx remotion still Couverture out/couverture.png --props=props/ma-couverture.json`

Pour ajouter une référence : `scripts/reference.sh <lien du reel>`, regarde `refs/<id>/planche.jpg` et `infos.txt`, puis ajoute une ligne au tableau de la partie 1.

## 6. Les outils

| Outil | À quoi il sert | Commande |
|---|---|---|
| **Remotion** 4.0.540 | Monter les reels en code (les 4 compositions ci-dessus) | `npm run studio`, `npx remotion render …` |
| **HyperFrames** 0.9.11 | Cartons et animations en HTML (`hyperframes/index.html` : accroche animée). Export `--format mov` avec fond transparent pour les poser dans CapCut | `cd hyperframes && npx hyperframes preview`, `npx hyperframes render` |
| **ffmpeg** | Couper, convertir, extraire le son | `ffmpeg -ss 12 -to 18 -i rush.mp4 -c copy extrait.mp4` |
| **Whisper** | Transcrire pour les sous-titres | `python3 scripts/sous-titres.py <vidéo>` |
| **yt-dlp** | Télécharger un reel de référence | `scripts/reference.sh <lien>` |

**Sur ton ordinateur** : Node 22 ou plus, ffmpeg, Python 3, puis
`pip install -U yt-dlp openai-whisper` et `cd video && npm install`.
Pour Instagram, yt-dlp a souvent besoin de tes cookies : `YTDLP_OPTS="--cookies-from-browser chrome" scripts/reference.sh <lien>`.

**Dans une session cloud Claude** : instagram.com est fermé, `scripts/reference.sh` passe alors par Apify (déjà connecté). Remotion utilise le Chromium du conteneur (voir `remotion.config.ts`). Pour HyperFrames, `export HYPERFRAMES_BROWSER_PATH=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell)` active le rendu rapide.

Licence : Remotion est gratuit pour une personne seule ou une entreprise de 3 personnes au plus, ce qui est ton cas.
