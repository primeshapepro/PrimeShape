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

1. Apify récupère les reels récents des hashtags et des comptes ci-dessus
   (c'est le « scroll »), avec vues, likes, commentaires, légende et vidéo.
2. Le script calcule le score de percée et garde les reels qui percent.
3. Claude regarde chaque reel retenu (légende, image, texte parlé) et ne garde
   que ceux qui entrent dans les piliers ci-dessus, avec pour chacun :
   l'accroche, pourquoi ça marche, et comment Andy peut le refaire.
4. Le résultat arrive dans un catalogue où Andy coche les reels à monter.

## Réglages nécessaires

Dans les réglages de l'environnement cloud :

- variable d'environnement ou secret `APIFY_TOKEN` (la clé API Apify) ;
- domaines autorisés : `api.apify.com`, et pour regarder les vidéos
  `cdninstagram.com` et `fbcdn.net`.
