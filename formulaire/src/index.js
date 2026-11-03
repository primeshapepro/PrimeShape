// Reçoit les formulaires du site PrimeShape et les envoie par email à Andy.
// Requête attendue : POST multipart/form-data ou urlencoded, champ « form-name » = contact | avis.
import { EmailMessage } from 'cloudflare:email';

const ORIGINS = [/^https:\/\/(www\.)?prime-shape\.fr$/, /^https:\/\/([a-z0-9-]+\.)?primeshape\.pages\.dev$/];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const FORMS = {
  contact: {
    required: ['prenom', 'email', 'consentement'],
    subject: (f) => `Nouveau contact PrimeShape : ${f.motif || 'Message'} (${f.prenom})`,
    lines: (f) => [
      ['Motif', f.motif], ['Prénom', f.prenom], ['Nom', f.nom], ['Email', f.email],
      ['Téléphone', f.telephone], ['Consentement', f.consentement ? 'oui' : 'non'], ['', ''], ['Message', f.message || '(aucun message)'],
    ],
  },
  avis: {
    required: ['note', 'prenom', 'email', 'experience', 'avis', 'consentement-publication'],
    subject: (f) => `Nouvel avis PrimeShape : ${f.note}/5 (${f.prenom})`,
    lines: (f) => [
      ['Note', `${f.note}/5`], ['Contexte', f.contexte], ['Prénom', f.prenom], ['Nom', f.nom], ['Email', f.email],
      ['Mois de l\'expérience', f.experience], ['Accord de publication', f['consentement-publication'] ? 'oui' : 'non'], ['', ''],
      ['Avis', f.avis], ['', ''], ['', 'À vérifier puis ajouter dans avis.json pour le publier.'],
    ],
  },
};

const LIMITS = { message: 2000, avis: 800, default: 200 };

function cors(origin) {
  const ok = origin && ORIGINS.some((re) => re.test(origin));
  return ok ? { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Accept, Content-Type', Vary: 'Origin' } : {};
}

function reply(request, env, status, body) {
  const origin = request.headers.get('Origin');
  const wantsJson = (request.headers.get('Accept') || '').includes('application/json');
  if (!wantsJson) {
    // Envoi sans JavaScript : on renvoie vers la page de confirmation du site
    return Response.redirect(`${env.SITE}/${status < 400 ? 'merci/' : '#contact'}`, 303);
  }
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...cors(origin) } });
}

// En-têtes d'email : sans retour à la ligne (pas d'injection), encodés en UTF-8
const clean = (v) => String(v || '').replace(/[\r\n]+/g, ' ').trim();
const b64 = (s) => { const bytes = new TextEncoder().encode(s); let bin = ''; for (const b of bytes) bin += String.fromCharCode(b); return btoa(bin); };
const encodeHeader = (s) => `=?UTF-8?B?${b64(clean(s))}?=`;

export function buildMessage({ from, to, replyTo, subject, text }) {
  const body = b64(text).replace(/.{1,76}/g, '$&\r\n');
  return [
    `From: PrimeShape <${from}>`,
    `To: ${to}`,
    replyTo ? `Reply-To: ${clean(replyTo)}` : null,
    `Subject: ${encodeHeader(subject)}`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@prime-shape.fr>`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    '',
    body,
  ].filter((l) => l !== null).join('\r\n');
}

export function readForm(data) {
  const kind = data.get('form-name');
  const spec = FORMS[kind];
  if (!spec) return { error: 'formulaire inconnu' };
  if (data.get('bot-field')) return { spam: true };
  const f = {};
  for (const [k, v] of data.entries()) {
    if (typeof v !== 'string') continue;
    f[k] = v.trim().slice(0, LIMITS[k] || LIMITS.default);
  }
  for (const k of spec.required) if (!f[k]) return { error: `champ manquant : ${k}` };
  if (!EMAIL_RE.test(f.email)) return { error: 'email invalide' };
  if (kind === 'avis' && !/^[1-5]$/.test(f.note)) return { error: 'note invalide' };
  const text = spec.lines(f).map(([k, v]) => (k ? `${k} : ${v || '-'}` : v)).join('\n') + '\n\n-- \nEnvoyé depuis le formulaire de prime-shape.fr. Réponds directement à cet email pour écrire à la personne.\n';
  return { kind, subject: spec.subject(f), text, replyTo: f.email };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin');
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(origin) });
    if (request.method !== 'POST') return new Response('PrimeShape : formulaires du site.', { status: 200 });
    if (origin && !ORIGINS.some((re) => re.test(origin))) return reply(request, env, 403, { ok: false, error: 'origine refusée' });

    let data;
    try { data = await request.formData(); } catch { return reply(request, env, 400, { ok: false, error: 'requête illisible' }); }
    const form = readForm(data);
    if (form.spam) return reply(request, env, 200, { ok: true });
    if (form.error) return reply(request, env, 400, { ok: false, error: form.error });

    try {
      const raw = buildMessage({ from: env.FROM, to: env.TO, replyTo: form.replyTo, subject: form.subject, text: form.text });
      await env.MAILER.send(new EmailMessage(env.FROM, env.TO, raw));
    } catch (err) {
      console.error('Envoi impossible', err);
      return reply(request, env, 502, { ok: false, error: 'envoi impossible' });
    }
    return reply(request, env, 200, { ok: true });
  },
};
