import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useVideoConfig} from 'remotion';
import {Accroche} from '../components/Accroche';
import {CarteFin} from '../components/CarteFin';
import {Rush} from '../components/Rush';
import {SousTitres} from '../components/SousTitres';
import {couleurs} from '../theme';
import type {Commun, Insert, Ligne} from '../types';

/**
 * Format « Face cam / Série » (refs @abigaildaniellla et @geoff.garlic) :
 * tu parles face caméra, sous-titres mot à mot, plans de coupe toutes les 2-3 s
 * pendant que ta voix continue, carton de série, puis DM.
 */
export type FaceCamProps = Commun & {
  video: string;
  debut?: number;
  duree?: number; // en secondes ; si absent, on prend la durée du rush
  sousTitres?: string;
  motsCles?: string[];
  titre?: {label?: string; lignes: Ligne[]; a: number; duree: number};
  inserts?: Insert[];
};

export const FaceCam: React.FC<FaceCamProps & {dureeRush: number}> = (props) => {
  const {video, debut = 0, dureeRush, sousTitres, motsCles, titre, inserts = [], look = 'noir', musique, volumeMusique = 0.25, fin} = props;
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const principal = f(dureeRush);

  return (
    <AbsoluteFill style={{backgroundColor: couleurs.noir}}>
      <Sequence durationInFrames={principal}>
        <Rush video={video} debut={debut} look={look} />
        {inserts.map((ins, i) => (
          <Sequence key={i} from={f(ins.a)} durationInFrames={f(ins.duree)}>
            <Rush video={ins.video} debut={ins.debut} muet look={look} />
          </Sequence>
        ))}
        {titre ? (
          <Sequence from={f(titre.a)} durationInFrames={f(titre.duree)}>
            <Accroche lignes={titre.lignes} label={titre.label} voile={0.45} />
          </Sequence>
        ) : null}
        {sousTitres ? <SousTitres fichier={sousTitres} motsCles={motsCles} decalageMs={debut * 1000} /> : null}
      </Sequence>

      <Sequence from={principal} durationInFrames={f(fin.duree)}>
        <CarteFin {...fin} />
      </Sequence>

      {musique ? (
        <Audio
          src={staticFile(musique)}
          volume={(i) => interpolate(i, [durationInFrames - 20, durationInFrames], [volumeMusique, 0], {extrapolateLeft: 'clamp'})}
        />
      ) : null}
    </AbsoluteFill>
  );
};
