# Design PrimeShape

Direction : des aplats de couleur, comme les toiles de Cézanne sur la Sainte-Victoire. Chaque section est un plan de couleur pleine. La profondeur vient du paysage : des plans de montagnes translucides superposés (perspective atmosphérique), et des panneaux de verre dépoli posés devant eux. Pas de dégradé, pas de grain, pas d'effet au survol au-delà d'un changement de couleur.

## Couleurs (imposées)

| Rôle | Valeur |
|---|---|
| Encre (fond principal) | `#16191f` |
| Ardoise (plan secondaire) | `#1e2330` |
| Vert (plan « Valeurs », boutons) | `#2e7d4f` |
| Vert clair (accent sur fond sombre) | `#4aa36e` |
| Vert foncé (accent sur fond clair) | `#29714a` |
| Calcaire (plan clair) | `#f2f1ee` |
| Texte secondaire sur sombre | `#b8bcc8`, discret `#979cab` |
| Texte secondaire sur clair | `#4a4f5c`, discret `#5f6474` |

Ordre des plans sur l'accueil : encre (héros) → ardoise → vert → calcaire → encre → ardoise → encre (contact) → encre (pied de page).

## Typographie (imposée)

- Titres : Nippo 700, capitales. `h1` jusqu'à 7.5rem, `.h2` `clamp(2rem, 4.2vw, 3.6rem)`, interlignage 0.92 à 1.
- Texte : Raleway, 1rem à 1.1rem (`.lead`), interlignage 1.75, 34rem de large au plus.
- Petites étiquettes (`.meta`) : Nippo 600, 0.78rem, capitales, interlettrage 0.08em. À utiliser rarement.

## Composants

- Bouton : pilule pleine verte (`.btn-green`) ou contour 1px (`.btn-line`), Nippo capitales 0.72rem.
- Séparateurs : filets de 1px (`--line` sur sombre, `--line-dark` sur clair).
- Verre (`.glass`) : fond blanc à 4,5 %, bordure blanche à 10 %, flou 20px, rayon 22px, ombre portée douce. Uniquement devant le paysage (formules, avis, formulaire de contact) et pour la barre une fois qu'on défile ; jamais sur un fond clair.
- Paysage (`.scape`) : 4 plans, du plus lointain au plus proche, vert à 8 %, vert à 13 %, Sainte-Victoire ardoise avec son arête verte, premier plan opaque de la couleur de la section suivante. En haut de page, les plans glissent à des vitesses différentes au défilement ; en bas de la section contact, ils sont fixes.
- Logo : trait de crête vert + PRIME (blanc) SHAPE (vert clair).
- Signature : le paysage en plans superposés en haut et en bas de page ; la trace du parcours qui se dessine au défilement.

## Espacements

Sections `.plane` : `clamp(5rem, 13vh, 9rem)` en haut et en bas. Marges latérales 48px, 32px en tablette, 20px en mobile. Grille 12 colonnes (4 en mobile).

## À ne pas faire

Écran de chargement, curseur personnalisé, texte qui défile, étiquettes au-dessus des titres, titres bicolores, texte en contour, cartes inclinées, apparitions animées sur chaque bloc.
