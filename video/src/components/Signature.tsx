import React from 'react';
import {couleurs, polices, reel} from '../theme';

export const IconeP: React.FC<{taille?: number}> = ({taille = 60}) => (
  <svg width={taille} height={taille} viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="ps-remplissage-p" x1="0" y1="1" x2="0" y2="0">
        <stop offset="0" stopColor={couleurs.vertSapin} />
        <stop offset="0.54" stopColor={couleurs.vertSapin} />
        <stop offset="0.54" stopColor={couleurs.vertSapin} stopOpacity="0" />
        <stop offset="1" stopColor={couleurs.vertSapin} stopOpacity="0" />
      </linearGradient>
    </defs>
    <rect x="0" y="0" width="100" height="100" rx="25.6" fill={couleurs.noir} />
    <rect x="7.3" y="7.3" width="85.4" height="85.4" rx="18.3" fill="none" stroke={couleurs.vertClair} strokeOpacity="0.55" strokeWidth="1.3" />
    <text
      x="50"
      y="48.8"
      textAnchor="middle"
      dominantBaseline="central"
      fontFamily="Nippo"
      fontWeight="700"
      fontSize="70.7"
      fill="url(#ps-remplissage-p)"
      stroke={couleurs.vertClair}
      strokeWidth="3.2"
      paintOrder="stroke"
    >
      P
    </text>
  </svg>
);

export const Logotype: React.FC<{taille?: number}> = ({taille = 28}) => (
  <div style={{fontFamily: polices.texte, fontWeight: 700, fontSize: taille, lineHeight: 1, letterSpacing: '0.12em', color: couleurs.blancOs, whiteSpace: 'nowrap'}}>
    PRIME<span style={{color: couleurs.vertClair}}>SHAPE</span>
  </div>
);

/** Pied de reel : logo à gauche, @PRIMESHAPEFR à droite, posé au-dessus de la zone sûre du bas. */
export const Signature: React.FC<{seulementCompte?: boolean}> = ({seulementCompte = false}) => (
  <div
    style={{
      position: 'absolute',
      left: reel.cote,
      right: reel.cote,
      bottom: reel.zoneBas,
      display: 'flex',
      alignItems: 'center',
      justifyContent: seulementCompte ? 'center' : 'space-between',
    }}
  >
    {seulementCompte ? null : (
      <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
        <IconeP />
        <Logotype />
      </div>
    )}
    <div style={{fontFamily: polices.texte, fontWeight: 500, fontSize: 28, lineHeight: 1, letterSpacing: '0.2em', color: couleurs.gris}}>
      @PRIMESHAPEFR
    </div>
  </div>
);
