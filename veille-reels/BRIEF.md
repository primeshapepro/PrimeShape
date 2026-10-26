# Veille reels PrimeShape : le brief

Ce dossier n'est pas publié sur le site (`build.sh` ne copie que les fichiers du site).

## Objectif

Chaque semaine, parcourir à la place d'Andy les reels Instagram de sa niche,
repérer ceux qui percent, et ne lui présenter que ceux qui ressemblent à ce qu'il
fait. Il choisit ensuite lesquels refaire à sa façon (on reprend l'idée,
l'accroche et le rythme, jamais la vidéo d'un autre).

## Ce qui correspond à Andy

Un reel est retenu s'il entre dans au moins un des trois piliers :

1. **Motivation** : se lancer, tenir dans la durée, reprendre après une pause.
2. **Exercices à la maison** : sans matériel ou presque, faisables par un débutant.
3. **Conseils santé** : hygiène de vie, sommeil, nutrition, sport et santé.

Et s'il parle au même public : débutants et adultes en reprise, 30 à 60 ans,
ton simple et bienveillant. On écarte le bodybuilding, la performance pure,
les promesses miracles et les transformations physiques mises en avant.
Le français passe en priorité ; un reel en anglais est gardé si l'idée se refait
facilement en français.

## Le score de percée

`vues du reel ÷ vues habituelles (médiane) du compte`

- à partir de ×3 : ça perce
- à partir de ×10 : viral
- uniquement les reels de moins de 30 jours

## Points de départ

Hashtags :
#remiseenforme #reprisedusport #sportdebutant #coachsportif #perdredupoids
#sportapres40ans #sportapres50ans #sportalamaison #exercicesalamaison
#motivationsport #hygienedevie #nutritionsante #reequilibragealimentaire
#fitnessfrance #over40fitness #beginnerworkout

Comptes vérifiés (abonnés approximatifs, octobre 2026) :

| Compte | Pourquoi |
| --- | --- |
| @lucilewoodward | sport, alimentation, mental (~320 k) |
| @sissymua | exercices à la maison, nutrition (~2 M) |
| @jujufitcats | exercices à la maison, motivation (~2,4 M) |
| @tiboinshape | motivation, nutrition, entraînement (le plus gros compte FR) |
| @myf_moveyourfit | programmes maison, reprise du sport, alimentation (~210 k) |
| @jessicamellet | coach diplômée d'État, perte de poids sans régime (~125 k) |
| @fitbyclem | renforcement et cardio pour les femmes (~265 k) |
| @majormouvement | kiné, santé du corps au quotidien (~320 k et plus) |
| @aimerycalkins | coach sportif et mobilité (~105 k) |
| @rudycoiasp | musculation et longévité (~75 k) |
| @kineparnature | kiné, conseils et exercices (~15 k) |
| @equipe.active | forme et bien-être après 50 ans (~3 k) |

Veille locale (Aix-en-Provence), pour voir ce que font les coachs du coin :
@theocoaching_aix, @fitness_nicolas, @davidvicard, @abccoachs.

## Comment ça tourne

1. `python3 veille-reels/collecte.py` (ou `--essai` pour un test à quelques
   centimes) récupère via Apify les reels récents des comptes suivis et des
   hashtags de `config.json` : c'est le « scroll ».
2. Le script calcule le score de percée et écrit `resultats/AAAA-MM-JJ.json`
   (non versionné : ce sont les données d'autres créateurs).
3. Claude regarde les reels retenus (légende, image de couverture) et ne garde
   que ceux qui entrent dans les piliers ci-dessus, avec pour chacun :
   l'accroche, pourquoi ça marche, et comment Andy peut le refaire.
4. Le résultat arrive dans un catalogue où Andy coche les reels à monter.

Ce que l'essai du 26 octobre 2026 a appris :

- Les hashtags renvoient les meilleurs reels des derniers mois, rarement ceux
  de la semaine. Ils servent à découvrir des comptes ; les reels de moins de
  120 jours qu'ils remontent sont gardés comme « formats qui ont cartonné ».
- Un format qui explose peut porter un contenu faux (astuces santé miracles) :
  on garde la structure, jamais les affirmations. Rien qui contredise la
  promesse « sans promesse miracle » de PrimeShape.
- Les comptes découverts pertinents sont à ajouter à `comptes` dans
  `config.json` au fil des semaines.

## Coût

Compte Apify gratuit : 5 $ de crédit par mois. Chaque reel coûte 0,0026 $.
Les réglages de `config.json` visent environ 450 reels par collecte, soit à
peu près 1,20 $ : une collecte par semaine reste dans le crédit gratuit.
La transcription des vidéos coûte 0,048 $ par minute : à réserver aux reels
retenus.

## Réglages de l'environnement cloud (faits)

- Secret réseau « Apify » sur `api.apify.com` : la clé est ajoutée aux
  requêtes sans apparaître dans la session (`APIFY_TOKEN` marche aussi).
- Domaines autorisés : `api.apify.com`, `*.cdninstagram.com`, `*.fbcdn.net`.
