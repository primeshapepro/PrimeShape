import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {couleurs, polices, reel} from '../theme';
import type {Ligne} from '../types';
import {Label} from './Label';

const styleLigne = (style: Ligne['style']): React.CSSProperties => {
  if (style === 'aplat') {
    return {color: couleurs.blanc, background: couleurs.vertSapin, padding: '4px 26px 12px', marginLeft: -26};
  }
  if (style === 'vert') return {color: couleurs.vertClair};
  return {color: couleurs.blancOs};
};

/**
 * Accroche des 2 premières secondes : capitales Clash Display, une idée par ligne,
 * le mot-clé sur aplat vert sapin. La 1re ligne est là tout de suite, les autres suivent.
 */
export const Accroche: React.FC<{
  lignes: Ligne[];
  label?: string;
  taille?: number;
  voile?: number; // 0 à 1 : assombrit la vidéo dessous pour que le texte se lise
  anime?: boolean; // false pour une image fixe (couverture)
}> = ({lignes, label, taille = 128, voile = 0, anime = true}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill>
      {voile > 0 ? <AbsoluteFill style={{backgroundColor: couleurs.noir, opacity: voile}} /> : null}
      <AbsoluteFill
        style={{
          padding: `${reel.zoneHaut}px ${reel.cote}px ${reel.zoneBas}px`,
          display: 'flex',
          flexDirection: 'column',
          gap: 48,
        }}
      >
        {/* sur une vidéo, le gris se perd : le label passe en blanc os */}
        {label ? <Label couleur={voile > 0 ? couleurs.blancOs : couleurs.gris} taille={28}>{label}</Label> : null}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            gap: 10,
            fontFamily: polices.titre,
            fontWeight: 500,
            fontSize: taille,
            lineHeight: 1.02,
            letterSpacing: '0.01em',
            textTransform: 'uppercase',
          }}
        >
          {lignes.map((ligne, i) => {
            // la 1re ligne est là dès l'image 0 (image du fil Instagram), les suivantes arrivent toutes les 4 images
            const p = anime && i > 0 ? spring({frame: frame - (i - 1) * 4, fps, config: {damping: 200}, durationInFrames: 10}) : 1;
            return (
              <div
                key={i}
                style={{
                  ...styleLigne(ligne.style),
                  whiteSpace: 'nowrap',
                  opacity: p,
                  transform: `translateY(${(1 - p) * 28}px)`,
                }}
              >
                {ligne.texte}
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
