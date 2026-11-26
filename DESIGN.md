# Design PrimeShape

Direction « studio » sur la charte Noir massif : site entièrement sombre (Andy ne veut ni sections claires, ni gris ardoise, ni orange), vert sapin et vert clair pour la marque, Clash Display pour les titres, Nippo pour le texte. Inspiration : un site de studio d'architecture vu sur TikTok, adapté à PrimeShape. Le thème reste la montée de la Sainte-Victoire, à deux.

## Couleurs

Jetons dans `:root` et `.t-dark` de `index.html` (mêmes valeurs dans `assets/pages.css`).

| Jeton | Valeur | Usage |
|---|---|---|
| `--noir` | `#0c0e0d` | Fond de toutes les sections |
| `--surface` | `#161a19` | Cartes (valeurs, formules, avis, formulaires, sections légales) |
| `--surface-2` | `#1f2422` | Carte au survol, numéros d'étape éteints |
| `--line` / `--line-2` | blanc os à 10 % / 20 % | Filets, contours de boutons |
| `--fg` | `#edeee9` blanc os | Titres, texte fort, bouton principal |
| `--soft` | `#b9bfba` | Texte courant |
| `--muted` | `#8d948f` | Étiquettes, légendes |
| `--vert` | `#4aa36e` vert clair | « Shape », points des étiquettes, numéros, étoiles, trace du parcours |
| `--sapin` | `#2e7d4f` vert sapin | Bouton principal au survol |

## Typographie

- Grands titres : Clash Display 500, interlettrage serré (-0.03 à -0.045em), casse normale.
- « PrimeShape » géant dans l'ouverture (jusqu'à 250px), « Shape » en vert.
- Textes qui s'allument : Clash Display 400, jusqu'à 56px.
- Étiquettes : Nippo 500, 14px, casse normale, précédées d'un petit point vert.
- Texte : Nippo 400, 16 à 18px.

## Composants

- Boutons en pastille : principal blanc os (vert sapin au survol), secondaire en contour fin.
- Cartes arrondies de 22 à 26px, sans grain ni pointillés.
- Sections qui « glissent » : bord arrondi en haut et ombre, elles passent par-dessus la précédente.
- Formules : trois cartes sans image (Essentiel, Premium, Partenariats). Texte à gauche, liste à droite, bouton en bas.
- En séance : les trois vidéos en image fixe avec un bouton lecture. Rien ne se lance tout seul : au clic, la vidéo s'ouvre en grand sur fond noir.
- FAQ : six questions qui se déplient.
- Logo : crête verte + PRIMESHAPE (SHAPE en vert).

## Animations

- Ouverture : la vidéo de coaching en plein écran (lecture automatique, sans son). Les lettres de « PrimeShape » apparaissent en fondu flou, l'heure à Aix s'affiche en haut à droite. Au défilement, la vidéo grossit et s'assombrit pendant que la section suivante glisse par-dessus.
- Qui je suis et Avis : les mots du grand texte s'allument un par un au défilement.
- Chiffres (1 011 m, 2 formules, note des avis) qui défilent jusqu'à leur valeur.
- En séance : une bande fine s'ouvre en grand sur les trois vidéos (section épinglée pendant le défilement).
- Formules : les cartes s'empilent ; la précédente recule et s'assombrit quand la suivante arrive.
- Parcours : la trace verte monte et allume les étapes.
- Blocs qui apparaissent en fondu en montant ; « Faisons connaissance. » arrive en fondu flou.
- Formulaires : trait vert sous le champ actif, champ en erreur qui tremble.
- Écran « Message envoyé » : halo vert, la crête se trace, le drapeau se plante, éclats, compte à rebours de 5 s.
- Écran « Merci pour ton avis » : les étoiles s'allument une à une jusqu'à la note donnée.
- Pages légales, 404 et merci : grand titre en fondu flou ; la crête se trace en bas sur 404 et merci.
- Tout est figé avec « réduire les animations ».

## Espacements

Sections : `clamp(96px, 15vh, 170px)` en haut et en bas. Marges latérales 56px, 40px en tablette, 20px en mobile. Contenu limité à 1320px.
