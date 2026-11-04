import React from 'react';
import {AbsoluteFill} from 'remotion';
import {couleurs, polices, reel} from '../theme';
import type {Fin} from '../types';
import {Accroche} from './Accroche';
import {Signature} from './Signature';

/** Dernier écran : l'invitation en DM, sur noir massif. */
export const CarteFin: React.FC<Fin> = ({lignes, texte}) => (
  <AbsoluteFill style={{backgroundColor: couleurs.noir}}>
    <Accroche lignes={lignes} taille={112} />
    <div
      style={{
        position: 'absolute',
        left: reel.cote,
        right: reel.cote,
        bottom: reel.zoneBas + 140,
        fontFamily: polices.texte,
        fontWeight: 400,
        fontSize: 42,
        lineHeight: 1.45,
        color: couleurs.texte,
      }}
    >
      {texte}
    </div>
    <Signature />
  </AbsoluteFill>
);
