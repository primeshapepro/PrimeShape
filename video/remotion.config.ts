import {Config} from '@remotion/cli/config';
import fs from 'node:fs';
import path from 'node:path';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(90);
Config.setOverwriteOutput(true);

// Dans le conteneur cloud, Remotion ne peut pas télécharger son navigateur :
// on lui donne le chrome-headless-shell déjà installé. Sur ton ordinateur, rien à faire.
const trouverNavigateur = (): string | null => {
  if (process.env.REMOTION_BROWSER && fs.existsSync(process.env.REMOTION_BROWSER)) {
    return process.env.REMOTION_BROWSER;
  }
  const racine = '/opt/pw-browsers';
  if (!fs.existsSync(racine)) return null;
  for (const dossier of fs.readdirSync(racine)) {
    if (!dossier.startsWith('chromium_headless_shell-')) continue;
    const binaire = path.join(racine, dossier, 'chrome-headless-shell-linux64', 'chrome-headless-shell');
    if (fs.existsSync(binaire)) return binaire;
  }
  return null;
};

const navigateur = trouverNavigateur();
if (navigateur) Config.setBrowserExecutable(navigateur);
