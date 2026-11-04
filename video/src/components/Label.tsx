import React from 'react';
import {couleurs, polices} from '../theme';

/** Petit label en capitales espacées, ex. « SÉRIE · REPRENDRE LE SPORT ». */
export const Label: React.FC<{children: React.ReactNode; couleur?: string; taille?: number}> = ({
  children,
  couleur = couleurs.gris,
  taille = 28,
}) => (
  <div
    style={{
      fontFamily: polices.texte,
      fontWeight: 500,
      fontSize: taille,
      lineHeight: 1,
      letterSpacing: '0.26em',
      textTransform: 'uppercase',
      color: couleur,
      whiteSpace: 'nowrap',
    }}
  >
    {children}
  </div>
);
