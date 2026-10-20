# Design PrimeShape

Direction : le carnet d'entraînement d'Andy. Le haut de page est la couverture (encre, élastique vert, étiquette collée), les sections sont les pages (papier calcaire quadrillé, marge verte), le pied de page est le dos du carnet. Les annotations sont faites au feutre vert et se tracent quand elles arrivent à l'écran.

## Couleurs (imposées)

| Rôle | Valeur |
|---|---|
| Encre : couverture, texte, en-tête de fiche | `#16191f` |
| Calcaire : papier des pages | `#f2f1ee` |
| Feuille posée (fiches, formulaire, avis) | `#fbfaf7` |
| Vert : élastique, boutons, intercalaire, coches | `#2e7d4f` |
| Vert clair : feutre, accent sur encre | `#4aa36e` |
| Vert foncé : texte vert sur papier | `#29714a` |
| Texte secondaire sur papier | `#464b57`, discret `#5f6474` |
| Texte secondaire sur encre | `#b8bcc8`, discret `#979cab` |
| Quadrillage | encre à 6 %, carreaux de 24px |
| Marge | vert à 50 %, 1,5px |

## Typographie

- Titres : Nippo 700, capitales (imposée). `h1` jusqu'à 6.4rem, `.h2` `clamp(2rem, 4.4vw, 3.6rem)`.
- Texte : Raleway (imposée), 1rem à 1.1rem, interlignage 1.75.
- Écriture à la main : Kalam 700 (`.hand`), uniquement pour des notes courtes : étiquette de couverture, légende de la photo, sous-titres des fiches, numéros d'étapes, phrases d'encouragement. Jamais pour un paragraphe ni un bouton.

## Matières et composants

- Couverture et dos : encre unie, élastique vert de 14px près du bord droit.
- Étiquette : papier calcaire réglé, tournée de -2°, ombre courte.
- Pages : quadrillage et marge verte continus sur toutes les sections claires ; un léger empilement de tranches de pages sous la couverture.
- Intercalaire (valeurs) : aplat vert pleine largeur.
- Feuilles posées (`.sheet`) : blanc cassé, ombre douce, légèrement tournées (±0,5 à 1°). Fiches de formules avec en-tête (encre pour Premium) et lignes cochées.
- Photo : la vidéo est une photo tirée sur papier blanc, scotchée par deux bandes vertes translucides, légende manuscrite.
- Traits au feutre (`.mark`) : cercle autour de « à deux. », soulignés sous certains mots, coches dans des cases dessinées. Ils se tracent une fois à l'écran ; déjà tracés si « réduire les animations ».
- Boutons : pilule verte pleine, ou contour encre 1.5px sur papier.
- Croquis du parcours : arête de la Sainte-Victoire au stylo, trace au feutre vert qui avance au défilement.

## Espacements

Pages `.page` : `clamp(4.5rem, 12vh, 8rem)` en haut et en bas. Marges latérales 48px, 40px en tablette, 22px en mobile. Contenu limité à 1200px.

## À ne pas faire

Verre dépoli, dégradés décoratifs, néon, écran de chargement, curseur personnalisé, texte qui défile, étiquettes au-dessus des titres, apparitions animées sur chaque bloc, Kalam en texte courant.
