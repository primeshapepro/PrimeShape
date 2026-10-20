# Design PrimeShape

Direction : des aplats de couleur, comme les toiles de Cézanne sur la Sainte-Victoire. Chaque section est un plan de couleur pleine, sans carte ni ornement. Sobre : pas d'ombre, pas de dégradé, pas de grain, pas d'effet au survol au-delà d'un changement de couleur.

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

Ordre des plans sur l'accueil : encre (héros) → ardoise → vert → calcaire → encre → ardoise → calcaire → encre (pied de page).

## Typographie (imposée)

- Titres : Nippo 700, capitales. `h1` jusqu'à 7.5rem, `.h2` `clamp(2rem, 4.2vw, 3.6rem)`, interlignage 0.92 à 1.
- Texte : Raleway, 1rem à 1.1rem (`.lead`), interlignage 1.75, 34rem de large au plus.
- Petites étiquettes (`.meta`) : Nippo 600, 0.78rem, capitales, interlettrage 0.08em. À utiliser rarement.

## Composants

- Bouton : pilule pleine verte (`.btn-green`) ou contour 1px (`.btn-line`), Nippo capitales 0.72rem.
- Séparateurs : filets de 1px (`--line` sur sombre, `--line-dark` sur clair). Pas de cartes.
- Logo : trait de crête vert + PRIME (blanc) SHAPE (vert clair).
- Signature : la crête de la Sainte-Victoire en aplat, frontière entre le héros et la section suivante ; la trace du parcours qui se dessine au défilement.

## Espacements

Sections `.plane` : `clamp(5rem, 13vh, 9rem)` en haut et en bas. Marges latérales 48px, 32px en tablette, 20px en mobile. Grille 12 colonnes (4 en mobile).

## À ne pas faire

Écran de chargement, curseur personnalisé, texte qui défile, étiquettes au-dessus des titres, titres bicolores, texte en contour, cartes inclinées, apparitions animées sur chaque bloc.
