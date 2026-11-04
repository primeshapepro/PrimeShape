import {parseMedia} from '@remotion/media-parser';
import React from 'react';
import {Composition, Still, staticFile} from 'remotion';
import {Citation, type CitationProps} from './formats/Citation';
import {Couverture, type CouvertureProps} from './formats/Couverture';
import {FaceCam, type FaceCamProps} from './formats/FaceCam';
import {Routine, dureeRoutine, type RoutineProps} from './formats/Routine';
import {reel} from './theme';
import type {Fin} from './types';

// Les valeurs ci-dessous sont des exemples (clip du site). Pour un vrai reel :
// mets tes rushes dans public/rushes/ et passe tes props avec --props=props/mon-reel.json

const finDM: Fin = {
  lignes: [{texte: 'Tu veux'}, {texte: 'reprendre ?'}, {texte: 'Écris-moi', style: 'aplat'}],
  texte: 'Envoie-moi un message en DM, on regarde ensemble par où commencer.',
  duree: 3,
};

const routine: RoutineProps = {
  serie: 'Série · Reprendre le sport',
  accroche: [{texte: '3 exos', style: 'aplat'}, {texte: 'pour'}, {texte: 'reprendre', style: 'vert'}, {texte: 'en douceur'}],
  dureeAccroche: 2.2,
  plans: [
    {video: 'demo/coaching.mp4', duree: 3, nom: 'Traction assistée', consigne: '3 × 6'},
    {video: 'demo/coaching.mp4', duree: 3, nom: 'Pompes sur genoux', consigne: '3 × 10'},
    {video: 'demo/coaching.mp4', duree: 3, nom: 'Fentes arrière', consigne: '3 × 8'},
  ],
  look: 'noir',
  fin: finDM,
};

const faceCam: FaceCamProps = {
  video: 'demo/coaching.mp4',
  sousTitres: 'sous-titres/demo.json',
  motsCles: ['sport', 'tiens'],
  titre: {label: 'Série · Reprendre le sport · Ép. 1', lignes: [{texte: 'Cette fois,'}, {texte: 'tu tiens.', style: 'aplat'}], a: 0, duree: 1.8},
  inserts: [],
  look: 'noir',
  fin: finDM,
};

const citation: CitationProps = {
  video: 'demo/coaching.mp4',
  duree: 3.7,
  texte: 'Le plus dur, ce n’est pas de commencer. C’est de revenir la semaine d’après.',
  look: 'noir',
};

const couverture: CouvertureProps = {
  serie: 'Série · Reprendre le sport',
  lignes: [{texte: '3 erreurs', style: 'aplat'}, {texte: 'quand tu'}, {texte: 'reprends', style: 'vert'}, {texte: 'le sport'}],
};

const dims = {width: reel.largeur, height: reel.hauteur, fps: reel.fps};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Routine"
      component={Routine}
      {...dims}
      durationInFrames={dureeRoutine(routine, reel.fps)}
      defaultProps={routine}
      calculateMetadata={({props}) => ({durationInFrames: dureeRoutine(props, reel.fps)})}
    />
    <Composition
      id="FaceCam"
      component={FaceCam}
      {...dims}
      durationInFrames={reel.fps * 10}
      defaultProps={{...faceCam, dureeRush: 0}}
      calculateMetadata={async ({props}) => {
        let dureeRush = props.duree;
        if (!dureeRush) {
          const {durationInSeconds} = await parseMedia({
            src: staticFile(props.video),
            fields: {durationInSeconds: true},
            acknowledgeRemotionLicense: true,
          });
          dureeRush = (durationInSeconds ?? 10) - (props.debut ?? 0);
        }
        return {
          durationInFrames: Math.round((dureeRush + props.fin.duree) * reel.fps),
          props: {...props, dureeRush},
        };
      }}
    />
    <Composition
      id="Citation"
      component={Citation}
      {...dims}
      durationInFrames={Math.round(citation.duree * reel.fps)}
      defaultProps={citation}
      calculateMetadata={({props}) => ({durationInFrames: Math.round(props.duree * reel.fps)})}
    />
    <Still id="Couverture" component={Couverture} width={reel.largeur} height={reel.hauteur} defaultProps={couverture} />
  </>
);
