// Charte PrimeShape « Noir massif » appliquée aux reels.
import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

export const couleurs = {
  noir: '#0C0E0D', // 60 % : fonds
  vertSapin: '#2E7D4F', // 25 % : aplat du mot-clé (texte blanc pur dessus)
  vertClair: '#4AA36E', // 10 % : mots-clés, consignes, « SHAPE »
  blancOs: '#EDEEE9', // 5 % : titres et textes sur noir
  gris: '#9AA09B',
  texte: '#C4C8C3',
  graphite: '#1A1E1C',
  bordure: '#2A2F2C',
  blanc: '#FFFFFF',
} as const;

export const polices = {
  titre: "'Clash Display', 'Trebuchet MS', sans-serif",
  texte: "'Nippo', 'Trebuchet MS', sans-serif",
} as const;

// 1080 × 1920, zones sûres Instagram : ~260 px en haut, ~380 px en bas.
export const reel = {largeur: 1080, hauteur: 1920, fps: 30, zoneHaut: 260, zoneBas: 380, cote: 72} as const;

// Étalonnage : « noir » = noirs plus denses, couleurs un peu éteintes (comme les refs salle de nuit).
export const looks = {
  noir: 'contrast(1.08) saturate(0.82) brightness(0.94)',
  naturel: 'none',
} as const;
export type Look = keyof typeof looks;

loadFont({family: 'Clash Display', url: staticFile('fonts/clash-display-variable.woff2'), weight: '200 700', format: 'woff2'});
loadFont({family: 'Nippo', url: staticFile('fonts/nippo-variable.woff2'), weight: '200 700', format: 'woff2'});
