import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useVideoConfig} from 'remotion';
import {looks, type Look} from '../theme';

/** Un rush plein cadre (recadré en 9:16), avec l'étalonnage de la charte. */
export const Rush: React.FC<{video: string; debut?: number; muet?: boolean; look?: Look; volume?: number}> = ({
  video,
  debut = 0,
  muet = false,
  look = 'noir',
  volume = 1,
}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <OffthreadVideo
        src={staticFile(video)}
        trimBefore={Math.round(debut * fps)}
        muted={muet}
        volume={volume}
        style={{width: '100%', height: '100%', objectFit: 'cover', filter: looks[look]}}
      />
    </AbsoluteFill>
  );
};
