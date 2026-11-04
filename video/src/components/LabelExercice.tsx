import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {couleurs, polices, reel} from '../theme';
import {Label} from './Label';

/**
 * Nom de l'exercice + consigne (« 3 × 10 »), discret, en haut du cadre :
 * comme dans les refs routine, le corps reste visible et c'est lui qui parle.
 */
export const LabelExercice: React.FC<{nom: string; consigne?: string; numero?: number; total?: number}> = ({
  nom,
  consigne,
  numero,
  total,
}) => {
  const frame = useCurrentFrame();
  const opacite = interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <div
      style={{
        position: 'absolute',
        top: reel.zoneHaut,
        left: reel.cote,
        right: reel.cote,
        display: 'flex',
        justifyContent: 'center',
        opacity: opacite,
      }}
    >
      <div
        style={{
          background: couleurs.noir,
          borderRadius: 14,
          padding: '18px 30px 20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 12,
        }}
      >
        {numero && total ? <Label taille={24}>{`Exo ${numero} / ${total}`}</Label> : null}
        <div style={{fontFamily: polices.texte, fontWeight: 600, fontSize: 46, lineHeight: 1.2, color: couleurs.blancOs, textAlign: 'center'}}>
          {nom}
          {consigne ? <span style={{color: couleurs.vertClair}}>{`  ${consigne}`}</span> : null}
        </div>
      </div>
    </div>
  );
};
