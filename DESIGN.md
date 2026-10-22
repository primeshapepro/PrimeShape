# Design PrimeShape

Direction : premium épuré, en thème sombre. Beaucoup d'espace, Nippo en graisse légère et en grand, une seule image forte (la vidéo de coaching), filets fins, boutons rectangulaires. Aucun effet : pas de verre, pas de halo, pas de dégradé, pas de néon, pas d'animation d'apparition.

## Couleurs (imposées)

Jetons sémantiques dans `:root`, inversés localement dans la section claire (`.values`).

| Jeton | Sombre (défaut) | Section claire |
|---|---|---|
| `--bg` fond | `#16191f` encre | `#f2f1ee` calcaire |
| `--bg-2` fond alterné (formules, contact) | `#1e2330` ardoise | — |
| `--fg` texte, filets forts, bouton principal | `#f2f1ee` | `#16191f` |
| `--text-2` texte courant | `#b8bcc8` | `#464b57` |
| `--text-3` texte discret | `#979cab` | `#5f6474` |
| `--rule` filets fins | calcaire à 16 % | encre à 16 % |
| `--accent` vert | `#4aa36e` | `#29714a` |

Ordre des sections : ouverture (encre) → qui je suis (encre) → valeurs (calcaire) → parcours (encre) → formules (ardoise) → avis (encre) → contact (ardoise) → pied de page (encre).

Le vert reste rare : logo, P des valeurs, trace du parcours, sous-titre Premium, survol des boutons.

## Typographie (imposée)

- Titres : Nippo 300, capitales. `h1` `clamp(2.8rem, 5.6vw, 5.4rem)` interlignage 1, dernière ligne en Nippo 600. `.h2` `clamp(2rem, 4vw, 3.4rem)`.
- Petits titres (faits, étapes) : Nippo 500, capitales, interlettrage 0.06em.
- Étiquettes et menu (`.meta`, `.nav`) : Nippo 500, 0.74rem, capitales, interlettrage 0.14em.
- Texte : Raleway, 1.08rem, interlignage 1.8.

## Composants

- Bouton principal : rectangle calcaire, texte encre, rayon 2px ; au survol, fond vert, texte blanc. Secondaire : contour 1px. Lien : texte souligné d'un filet.
- Ouverture : texte à gauche, vidéo pleine hauteur à droite sous la barre ; en mobile, la vidéo passe dessous en pleine largeur.
- Colonnes séparées par des filets de 1px ; jamais de cartes ni d'ombres.
- Vidéo : muette, en boucle, lecture seulement à l'écran, arrêtée avec « réduire les animations ».
- Légende de la vidéo : étiquette encre en bas à gauche (« En séance · Première traction »), style cartel de galerie.
- Logotype géant en filigrane : PRIME / SHAPE sur deux lignes (`clamp(6rem, 29vw, 26rem)`, calcaire à 6 %, décoratif, masqué aux lecteurs d'écran), entre le fond des sections et leur contenu. Il part du haut de l'écran et descend au fil du défilement jusqu'au pied de page ; la section claire passe par-dessus. Avec « réduire les animations », il reste fixe en bas.
- Animations de défilement : la trace du parcours et la descente du logotype en filigrane. Micro-interactions au survol uniquement : filet sous les liens du menu, soulignement des liens qui se retrace, bouton vert foncé à l'appui.
- Surfaces du navigateur : barre de défilement fine aux couleurs du thème, curseur de saisie et cases en vert.

## Espacements

Sections `.section` : `clamp(6rem, 16vh, 10.5rem)` en haut et en bas. Marges latérales 56px, 40px en tablette, 22px en mobile. Contenu limité à 1280px. Gouttière 32px.
