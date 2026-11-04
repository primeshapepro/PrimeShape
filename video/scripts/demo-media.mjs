// Copie le clip du site (media/coaching.mp4) dans public/demo/ pour les exemples du Studio.
import {copyFileSync, existsSync, mkdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const source = join(ici, '..', '..', 'media', 'coaching.mp4');
const dossier = join(ici, '..', 'public', 'demo');
if (existsSync(source)) {
  mkdirSync(dossier, {recursive: true});
  copyFileSync(source, join(dossier, 'coaching.mp4'));
}
