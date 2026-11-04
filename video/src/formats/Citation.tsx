import React from 'react';
import {AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Rush} from '../components/Rush';
import {Signature} from '../components/Signature';
import {couleurs, polices, reel, type Look} from '../theme';

/**
 * Format « Citation » (ref @vision9motion) : 6 à 10 s, un seul plan d'ambiance,
 * une phrase courte en petit, rien d'autre. Fait pour tourner en boucle.
 */
export type CitationProps = {
  video: string;
  debut?: number;
  duree: number;
  texte: string;
  voile?: number; // 0 à 1 : assombrit le plan ; choisis de préférence un plan déjà sombre
  look?: Look;
  musique?: string;
  volumeMusique?: number;
};

export const Citation: React.FC<CitationProps> = ({video, debut, texte, voile = 0.45, look = 'noir', musique, volumeMusique = 0.6}) => {
  const frame = useCurrentFrame();
  const opacite = interpolate(frame, [0, 15], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: couleurs.noir}}>
      <Rush video={video} debut={debut} look={look} muet={Boolean(musique)} />
      <AbsoluteFill style={{backgroundColor: couleurs.noir, opacity: voile}} />
      <div
        style={{
          position: 'absolute',
          top: 560,
          left: reel.cote + 80,
          right: reel.cote + 80,
          textAlign: 'center',
          fontFamily: polices.texte,
          fontWeight: 400,
          fontSize: 44,
          lineHeight: 1.45,
          color: couleurs.blancOs,
          opacity: opacite,
        }}
      >
        {texte}
      </div>
      <Signature seulementCompte />
      {musique ? <Audio src={staticFile(musique)} volume={volumeMusique} /> : null}
    </AbsoluteFill>
  );
};
