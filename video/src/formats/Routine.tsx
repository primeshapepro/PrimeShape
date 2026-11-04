import React from 'react';
import {AbsoluteFill, Audio, Sequence, Series, interpolate, staticFile, useVideoConfig} from 'remotion';
import {Accroche} from '../components/Accroche';
import {CarteFin} from '../components/CarteFin';
import {LabelExercice} from '../components/LabelExercice';
import {Rush} from '../components/Rush';
import {couleurs} from '../theme';
import type {Commun, Ligne, Plan} from '../types';

/**
 * Format « Routine » (refs @trains_gains et @victorialvt) :
 * accroche 2 s → un plan fixe par exercice, coupé sec, nom + consigne discrets → DM.
 */
export type RoutineProps = Commun & {
  serie?: string;
  accroche: Ligne[];
  dureeAccroche: number;
  plans: Plan[];
};

export const dureeRoutine = (p: RoutineProps, fps: number) =>
  Math.round((p.plans.reduce((t, plan) => t + plan.duree, 0) + p.fin.duree) * fps);

export const Routine: React.FC<RoutineProps> = (props) => {
  const {serie, accroche, dureeAccroche, plans, look = 'noir', musique, volumeMusique = 0.6, fin} = props;
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const finAccroche = f(dureeAccroche);
  const exercices = plans.filter((p) => p.nom).length;

  let curseur = 0;
  let numero = 0;
  const debuts = plans.map((p) => {
    const d = curseur;
    curseur += f(p.duree);
    return d;
  });

  return (
    <AbsoluteFill style={{backgroundColor: couleurs.noir}}>
      <Series>
        {plans.map((plan, i) => {
          if (plan.nom) numero += 1;
          // le label attend la fin de l'accroche s'ils se chevauchent
          const retardLabel = Math.max(0, finAccroche - debuts[i]);
          return (
            <Series.Sequence key={i} durationInFrames={f(plan.duree)}>
              <Rush video={plan.video} debut={plan.debut} muet={plan.muet} look={look} />
              {plan.nom && retardLabel < f(plan.duree) ? (
                <Sequence from={retardLabel} layout="none">
                  <LabelExercice nom={plan.nom} consigne={plan.consigne} numero={numero} total={exercices} />
                </Sequence>
              ) : null}
            </Series.Sequence>
          );
        })}
        <Series.Sequence durationInFrames={f(fin.duree)}>
          <CarteFin {...fin} />
        </Series.Sequence>
      </Series>

      <Sequence durationInFrames={finAccroche}>
        <Accroche lignes={accroche} label={serie} voile={0.6} />
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
