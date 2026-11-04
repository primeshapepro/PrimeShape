import type {Look} from './theme';

/** Une ligne d'accroche. « aplat » = mot-clé blanc sur vert sapin, « vert » = vert clair. */
export type Ligne = {texte: string; style?: 'normal' | 'vert' | 'aplat'};

/** Un plan monté bout à bout. Temps en secondes. */
export type Plan = {
  video: string; // chemin dans public/, ex. "rushes/tractions.mp4"
  debut?: number; // où commencer dans le rush
  duree: number;
  nom?: string; // nom de l'exercice, ex. "Pompes sur genoux"
  consigne?: string; // ex. "3 × 10" ou "30 s"
  muet?: boolean;
};

/** Un plan de coupe posé par-dessus la face cam (le son de la face cam continue). */
export type Insert = {video: string; a: number; duree: number; debut?: number};

export type Fin = {lignes: Ligne[]; texte: string; duree: number};

export type Commun = {look?: Look; musique?: string; volumeMusique?: number; fin: Fin};
