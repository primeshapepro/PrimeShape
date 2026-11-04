import {createTikTokStyleCaptions, type Caption, type TikTokPage} from '@remotion/captions';
import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Sequence, cancelRender, continueRender, delayRender, staticFile, useVideoConfig} from 'remotion';
import {couleurs, polices, reel} from '../theme';

const normaliser = (mot: string) =>
  mot
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]/g, '');

// Whisper sort parfois « ? » ou « ! » comme un mot à part : on le recolle au mot d'avant
// (avec une espace insécable, à la française) pour qu'il ne commence jamais une pastille.
const recollerPonctuation = (mots: Caption[]): Caption[] =>
  mots.reduce<Caption[]>((acc, mot) => {
    const seul = mot.text.trim();
    const precedent = acc[acc.length - 1];
    if (precedent && /^[?!:;»%…]+$/.test(seul)) {
      acc[acc.length - 1] = {...precedent, text: precedent.text + ' ' + seul, endMs: mot.endMs};
    } else {
      acc.push(mot);
    }
    return acc;
  }, []);

const Page: React.FC<{page: TikTokPage; motsCles: Set<string>; haut: number}> = ({page, motsCles, haut}) => (
  <AbsoluteFill style={{top: haut, bottom: 'auto', height: 'auto', alignItems: 'center', paddingLeft: reel.cote, paddingRight: reel.cote}}>
    <div
      style={{
        background: couleurs.noir,
        borderRadius: 14,
        padding: '20px 32px',
        fontFamily: polices.texte,
        fontWeight: 600,
        fontSize: 54,
        lineHeight: 1.25,
        color: couleurs.blancOs,
        textAlign: 'center',
        maxWidth: reel.largeur - reel.cote * 2,
      }}
    >
      {page.tokens.map((t, i) => (
        <span key={i} style={{whiteSpace: 'pre', color: motsCles.has(normaliser(t.text)) ? couleurs.vertClair : undefined}}>
          {i === 0 ? t.text.trimStart() : t.text}
        </span>
      ))}
    </div>
  </AbsoluteFill>
);

/**
 * Sous-titres mot à mot (1 à 3 mots à la fois, comme dans les refs face cam),
 * sur pastille noire, mots-clés en vert clair. Le fichier vient de scripts/sous-titres.py.
 */
export const SousTitres: React.FC<{
  fichier: string; // ex. "sous-titres/face-cam.json"
  motsCles?: string[];
  regroupementMs?: number; // plus grand = plus de mots par pastille
  haut?: number; // position verticale de la pastille
  decalageMs?: number; // si la face cam est coupée au début (debut du rush)
}> = ({fichier, motsCles = [], regroupementMs = 500, haut = 1180, decalageMs = 0}) => {
  const {fps} = useVideoConfig();
  const [mots, setMots] = useState<Caption[] | null>(null);
  const [attente] = useState(() => delayRender(`Sous-titres ${fichier}`));

  useEffect(() => {
    fetch(staticFile(fichier))
      .then((r) => r.json())
      .then((data: Caption[]) => {
        setMots(data);
        continueRender(attente);
      })
      .catch((e) => cancelRender(e));
  }, [fichier, attente]);

  const pages = useMemo(
    () =>
      mots ? createTikTokStyleCaptions({captions: recollerPonctuation(mots), combineTokensWithinMilliseconds: regroupementMs}).pages : [],
    [mots, regroupementMs],
  );
  const cles = useMemo(() => new Set(motsCles.map(normaliser)), [motsCles]);

  return (
    <AbsoluteFill>
      {pages.map((page, i) => {
        const suivante = pages[i + 1];
        const debutMs = page.startMs - decalageMs;
        const finMs = (suivante ? suivante.startMs : page.startMs + page.durationMs) - decalageMs;
        const de = Math.round((debutMs / 1000) * fps);
        const duree = Math.round((finMs / 1000) * fps) - de;
        if (duree <= 0 || de + duree <= 0) return null;
        return (
          <Sequence key={i} from={de} durationInFrames={duree} layout="none">
            <Page page={page} motsCles={cles} haut={haut} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
