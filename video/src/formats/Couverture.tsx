import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {Accroche} from '../components/Accroche';
import {Signature} from '../components/Signature';
import {couleurs, looks} from '../theme';
import type {Ligne} from '../types';

/** Couverture du reel (image fixe 1080 × 1920) : la même accroche que la vidéo. */
export type CouvertureProps = {serie?: string; lignes: Ligne[]; image?: string};

export const Couverture: React.FC<CouvertureProps> = ({serie, lignes, image}) => (
  <AbsoluteFill style={{backgroundColor: couleurs.noir}}>
    {image ? <Img src={staticFile(image)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: looks.noir}} /> : null}
    <Accroche lignes={lignes} label={serie} taille={150} voile={image ? 0.55 : 0} anime={false} />
    <Signature />
  </AbsoluteFill>
);
