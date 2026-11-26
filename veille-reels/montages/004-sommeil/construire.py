"""Montage #004 : « 8 habitudes pour mieux dormir », version PrimeShape du tableau du sommeil.

Construit la page HyperFrames (reel 1080 x 1920, 12 s, sans son) :

    python3 veille-reels/montages/004-sommeil/construire.py <icônes lucide-static> <index.html>

Le dossier de l'index.html doit contenir assets/ avec gsap.min.js, nippo-variable.woff2
(fonts/ du site) et clash-display.woff2 (police du catalogue). Rendu :

    npx hyperframes@0.8.150 render -o sommeil.mp4 -f 30

Les icônes Lucide sont copiées en SVG dans la page (pas de fichier externe à charger).
"""

import re
import sys
from pathlib import Path

ICONES, SORTIE = Path(sys.argv[1]), Path(sys.argv[2])

# Du matin au soir : une bonne nuit se prépare dès le matin.
# Seulement des conseils solides (pas de magnésium ni de tisane, dont l'effet n'est pas prouvé pour tous).
LIGNES = [
    ("alarm-clock", "Te lever à la même heure, même le week-end", "Horloge interne stable"),
    ("sun", "10 minutes de lumière du jour le matin", "Sommeil au bon moment le soir"),
    ("footprints", "Bouger dans la journée (marche, sport)", "Sommeil plus profond"),
    ("coffee", "Pas de café après 14 h", "Tu t'endors plus vite"),
    ("utensils", "Dîner léger, 2 à 3 h avant de dormir", "Ventre léger au coucher"),
    ("wine-off", "Pas d'alcool le soir", "Sommeil plus réparateur"),
    ("smartphone", "Écrans coupés 30 min avant de dormir", "Cerveau qui décroche"),
    ("thermometer-snowflake", "Chambre fraîche et noire (18‑19 °C)", "Moins de réveils la nuit"),
]


def icone(nom, classe="ico"):
    svg = (ICONES / f"{nom}.svg").read_text()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    # Seulement sur la balise <svg> : les <rect> de certaines icônes ont besoin de leurs width/height.
    ouverture = re.match(r"<svg[^>]*>", svg).group(0)
    nettoyee = re.sub(r'\s(width|height|class)="[^"]*"', "", ouverture)
    return svg.replace(ouverture, nettoyee.replace("<svg", f'<svg class="{classe}" aria-hidden="true"', 1), 1)


FLECHE = icone("arrow-right", "fleche")

lignes_html = "\n".join(
    f"""        <div class="ligne" id="ligne{i}">
          <div class="pastille">{icone(nom)}</div>
          <p class="habitude">{habitude}</p>
          {FLECHE}
          <p class="effet">{effet}</p>
        </div>"""
    for i, (nom, habitude, effet) in enumerate(LIGNES, start=1)
)

DUREE = 12

page = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Nippo";
        src: url("assets/nippo-variable.woff2") format("woff2");
        font-weight: 200 700;
        font-display: block;
      }}
      @font-face {{
        font-family: "Clash Display";
        src: url("assets/clash-display.woff2") format("woff2");
        font-weight: 200 700;
        font-display: block;
      }}
      :root {{
        --noir: #0c0e0d;
        --vert-sapin: #2e7d4f;
        --vert-clair: #4aa36e;
        --blanc-os: #edeee9;
        --gris: #9aa09b;
        --texte: #c4c8c3;
        --graphite: #1a1e1c;
        --bordure: #2a2f2c;
        --filigrane: #141816;
      }}
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--noir);
      }}
      #root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        background: var(--noir);
        font-family: "Nippo", "Trebuchet MS", sans-serif;
        color: var(--blanc-os);
      }}
      /* Gros 8 décoratif en filigrane, coupé par le bord droit. */
      #filigrane {{
        position: absolute;
        right: -170px;
        top: 160px;
        font-family: "Clash Display", "Trebuchet MS", sans-serif;
        font-weight: 600;
        font-size: 1500px;
        line-height: 1;
        color: var(--filigrane);
      }}
      /* Zones sûres d'un reel : rien d'important au-dessus de 250 px ni sous 1540 px. */
      #contenu {{
        position: absolute;
        left: 92px;
        right: 92px;
        top: 250px;
      }}
      .label {{
        font-weight: 500;
        font-size: 25px;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--vert-clair);
      }}
      #titre {{
        margin-top: 22px;
        font-family: "Clash Display", "Trebuchet MS", sans-serif;
        font-weight: 500;
        font-size: 92px;
        line-height: 1.04;
        letter-spacing: 0.01em;
        text-transform: uppercase;
        color: var(--blanc-os);
      }}
      #titre .aplat {{
        display: inline-block;
        background: var(--vert-sapin);
        color: #ffffff;
        padding: 0 18px 4px;
        margin-left: -4px;
        border-radius: 14px;
      }}
      #sous-titre {{
        margin-top: 22px;
        font-size: 31px;
        line-height: 1.4;
        color: var(--texte);
      }}
      #colonnes {{
        display: flex;
        margin-top: 40px;
        padding: 0 26px 0 128px;
        font-weight: 500;
        font-size: 21px;
        letter-spacing: 0.26em;
        text-transform: uppercase;
        color: var(--gris);
      }}
      #colonnes span:first-child {{
        width: 392px;
      }}
      #colonnes span:last-child {{
        margin-left: 66px;
      }}
      #tableau {{
        margin-top: 14px;
        display: flex;
        flex-direction: column;
        gap: 8px;
      }}
      .ligne {{
        display: flex;
        align-items: center;
        height: 90px;
        padding: 0 22px 0 16px;
        background: var(--graphite);
        border: 2px solid var(--bordure);
        border-radius: 20px;
      }}
      .pastille {{
        flex: none;
        width: 64px;
        height: 64px;
        display: grid;
        place-items: center;
        border-radius: 16px;
        background: var(--vert-sapin);
      }}
      .ico {{
        width: 36px;
        height: 36px;
        color: #ffffff;
        stroke-width: 2;
      }}
      .habitude {{
        width: 380px;
        margin-left: 24px;
        font-weight: 600;
        font-size: 29px;
        line-height: 1.18;
        color: var(--blanc-os);
      }}
      .fleche {{
        flex: none;
        width: 34px;
        height: 34px;
        margin: 0 16px;
        color: var(--vert-clair);
        stroke-width: 2.5;
      }}
      .effet {{
        flex: 1;
        font-weight: 400;
        font-size: 28px;
        line-height: 1.18;
        color: var(--vert-clair);
      }}
      #pied {{
        position: absolute;
        left: 92px;
        right: 92px;
        top: 1478px;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }}
      #logo {{
        font-weight: 700;
        font-size: 34px;
        letter-spacing: 0.12em;
        color: var(--blanc-os);
      }}
      #logo span {{
        color: var(--vert-clair);
      }}
      #compte {{
        font-weight: 500;
        font-size: 24px;
        letter-spacing: 0.2em;
        color: var(--gris);
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{DUREE}"
      data-width="1080"
      data-height="1920"
    >
      <div id="filigrane" aria-hidden="true">8</div>
      <div id="contenu">
        <p class="label" id="label">Sommeil · À enregistrer</p>
        <h1 id="titre">8 habitudes pour<br />mieux <span class="aplat">dormir.</span></h1>
        <p id="sous-titre">Une bonne nuit se prépare dès le matin.</p>
        <div id="colonnes"><span>Habitude</span><span>Effet</span></div>
        <div id="tableau">
{lignes_html}
        </div>
      </div>
      <div id="pied">
        <p id="logo">PRIME<span>SHAPE</span></p>
        <p id="compte">@PRIMESHAPEFR</p>
      </div>
    </div>

    <script>
      // 0 s : l'accroche est déjà lisible (c'est elle qui retient dans les 2 premières secondes).
      // 0,9 s puis toutes les 0,55 s : une ligne du tableau, l'habitude puis son effet.
      // De 5,6 s à la fin : le tableau complet reste à l'écran, le temps de le lire ou de l'enregistrer.
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#filigrane", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.2, ease: "power1.out" }}, 0);
      tl.fromTo("#titre .aplat", {{ scale: 0.92 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)" }}, 0.15);
      tl.fromTo("#colonnes", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.6);
      for (let i = 1; i <= {len(LIGNES)}; i++) {{
        const t = 0.9 + (i - 1) * 0.55;
        tl.fromTo("#ligne" + i, {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }}, t);
        tl.fromTo(
          "#ligne" + i + " .fleche, #ligne" + i + " .effet",
          {{ opacity: 0, x: -16 }},
          {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }},
          t + 0.18
        );
      }}
      tl.fromTo("#pied", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, 5.6);
      // Petit rappel visuel pendant la pause : les pastilles s'allument une à une.
      for (let i = 1; i <= {len(LIGNES)}; i++) {{
        tl.fromTo(
          "#ligne" + i + " .pastille",
          {{ backgroundColor: "#2e7d4f" }},
          {{ backgroundColor: "#4aa36e", duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }},
          6.6 + (i - 1) * 0.18
        );
      }}
      tl.set({{}}, {{}}, {DUREE});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

SORTIE.write_text(page)
print(f"{SORTIE} : {len(LIGNES)} lignes, {DUREE} s")
