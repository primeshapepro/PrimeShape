# Design PrimeShape

Direction « Noir massif », la même que la charte Instagram : fond noir, vert sapin et vert clair, Clash Display pour les titres, Nippo pour le texte. Site entièrement sombre (Andy ne veut pas de sections claires). Le thème : la montée de la Sainte-Victoire, à deux.

## Couleurs

Jetons dans `:root` de `index.html`.

| Jeton | Valeur | Usage |
|---|---|---|
| `--bg` | `#0c0e0d` noir | Fond de toutes les sections |
| `--card` | `#1a1e1c` graphite | Cartes (valeurs, formule Essentiel, avis, formulaires) |
| `--rule` | `#2a2f2c` | Contours de cartes et filets entre sections |
| `--fg` | `#edeee9` blanc os | Titres, texte fort, bouton principal |
| `--text-2` | `#c4c8c3` | Texte courant |
| `--text-3` | `#9aa09b` | Texte discret, étiquettes |
| `--accent` | `#4aa36e` vert clair | Mots-clés, étoiles, traces, petits titres |
| `--green` | `#2e7d4f` vert sapin | Aplat de la formule Premium |

## Typographie

- Titres : Clash Display 500, en minuscules (casse normale), interlettrage serré (-0.02em). `h1` jusqu'à 7.8rem, « à deux. » en vert. `.h2` `clamp(2.4rem, 5.6vw, 5rem)`.
- Petits titres au-dessus des titres (`.kick`) : Nippo 500, capitales, vert, interlettrage 0.3em.
- Étiquettes (`.meta`, menu, boutons) : Nippo 500 à 600, capitales, interlettrage 0.14 à 0.22em.
- Texte : Nippo 400, interlignage 1.75.

## Composants

- Boutons en pastille (rayon 999px) : principal blanc os, vert au survol ; secondaire en contour fin, vert au survol. Pendant un envoi, un cercle tourne à la place de la flèche.
- Cartes graphite à contour 1 ou 2 px, rayon 20 à 22 px. Formule Premium en aplat vert sapin.
- Logo : crête verte + PRIMESHAPE (SHAPE en vert) + « Coaching sportif » en gris, sans trait entre les deux.
- Grain d'impression très léger sur tout le site.
- Grands mots en pointillés (PRIMESHAPE dans l'ouverture et en pied de page).
- Section « En séance » : titre et texte à gauche (collés en haut au défilement), vidéos au format reel 9/16 à droite, en cartes arrondies ; aperçu muet qui se lance à l'écran, bouton lecture rond, titre en bas de la carte. Au clic, la vidéo s'ouvre en grand sur fond noir. Sur téléphone, défilement horizontal au doigt. Entrée en éventail au défilement.

## Animations

- Ouverture : le titre monte mot par mot ; la crête du logo, en très grand, se trace en vert ; deux points (la cordée) montent jusqu'au sommet avec un compteur d'altitude jusqu'à 1011 m ; un drapeau se plante et un cercle pulse. Le relief bouge légèrement avec la souris et au défilement.
- Jauge d'altitude fixe à droite (0 m en haut de la page, 1011 m en bas) ; sur téléphone et tablette, fine barre verte en haut de l'écran.
- Au défilement : titres mot par mot, textes en fondu, vidéo qui s'ouvre de bas en haut, cartes qui arrivent en décalé, formules qui basculent puis s'inclinent sous la souris, avis qui arrivent un par un.
- Parcours : la trace verte se dessine avec le défilement et allume chaque étape.
- Formulaires : trait vert qui se trace sous le champ actif, pastilles qui rebondissent, champ en erreur qui tremble, étoiles qui grossissent au survol.
- Écran « Message envoyé » : halo vert, la crête se trace, le drapeau se plante au sommet, des éclats partent du sommet, le titre monte, compte à rebours de 5 s puis retour en haut de l'accueil.
- Écran « Merci pour ton avis » : les étoiles s'allument une à une jusqu'à la note donnée, puis des éclats en partent ; 6 s avant le retour.
- Bandeau « Chaque sommet se gravit à deux » qui défile sous le contact.
- Tout est figé avec « réduire les animations ».

## Espacements

Sections : `clamp(90px, 16vh, 170px)` en haut et en bas, filet entre chaque section. Marges latérales 56px, 40px en tablette, 20px en mobile. Contenu limité à 1280px.
