"""Met à jour le fichier de suivi Instagram d'Andy à partir de son compte @primeshapefr.

    python3 veille-reels/suivi.py etat <suivi.xlsx> <reels.json>
        Liste les reels du compte absents du suivi, et ceux dont les chiffres sont à relever.

    python3 veille-reels/suivi.py appliquer <suivi.xlsx> <sortie.xlsx> <reels.json> [plan.json]
        Inscrit les nouvelles publications décrites dans plan.json, puis relève les chiffres.

reels.json : résultat brut d'apify~instagram-reel-scraper sur « primeshapefr ».
La correspondance numéro du planning -> code du reel est dans suivi-correspondances.json.

plan.json, une entrée par nouveau reel, écrite par Claude après l'avoir regardé :
    {"publications": [{"code": "De_z4lso99N", "numero": null,
                       "serie": "La motivation", "episode": "Bonus", "format": "Reel avec tes vidéos",
                       "sujet": "...", "accroche": "...", "appel": "—", "lien": "...", "notes": "..."}]}
« numero » vaut le N° d'une idée déjà au planning que la vidéo réalise (la ligne passe en
« Publié » à la date réelle), ou null pour ajouter une ligne.

Relevé des chiffres (vues, j'aime, commentaires ; le reste n'est visible que dans les statistiques
Instagram d'Andy) : à la publication, puis une dernière fois dès 7 jours, comme le demande l'onglet
Statistiques. Une note contenant « relevé final » ne bouge plus.
"""

import json
import sys
from copy import copy
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

PARIS = ZoneInfo("Europe/Paris")
CORRESPONDANCES = Path(__file__).resolve().parent / "suivi-correspondances.json"
FINAL = "relevé final"

JOUR = '=IF(B{r}="","",CHOOSE(WEEKDAY(B{r},2),"Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"))'
SEMAINE = '=IF(B{r}="","",IF(B{r}<$C$3,"Lancement","S"&(INT((B{r}-$C$3)/7)+1)))'
STATS = {
    2: '=IF($A{r}="","",IFERROR(INDEX(Planning!$H$6:$H$200,MATCH($A{r},Planning!$A$6:$A$200,0)),"N° introuvable"))',
    3: '=IF($A{r}="","",IFERROR(INDEX(Planning!$B$6:$B$200,MATCH($A{r},Planning!$A$6:$A$200,0)),""))',
    4: '=IF($A{r}="","",IFERROR(INDEX(Planning!$E$6:$E$200,MATCH($A{r},Planning!$A$6:$A$200,0)),""))',
    12: '=IF(F{r}="","",IFERROR((G{r}+H{r}+I{r}+J{r})/F{r},""))',
}


def code(reel):
    return reel["url"].rstrip("/").split("/")[-1]


def heure_paris(reel):
    return datetime.fromisoformat(reel["timestamp"].replace("Z", "+00:00")).astimezone(PARIS)


def vues(reel):
    return reel.get("videoPlayCount") or reel.get("videoViewCount") or 0


def charger_reels(fichier):
    return {code(r): r for r in json.loads(Path(fichier).read_text()) if r.get("url") and r.get("timestamp")}


def ligne_du_numero(ws, n, premiere):
    for r in range(premiere, ws.max_row + 1):
        if ws.cell(r, 1).value == n:
            return r
    return None


def premiere_ligne_libre(ws, premiere, colonnes):
    r = premiere
    while any(ws.cell(r, c).value not in (None, "") for c in colonnes):
        r += 1
    return r


def copier_style(ws, source, cible, colonnes):
    for c in colonnes:
        s, d = ws.cell(source, c), ws.cell(cible, c)
        d.font, d.alignment, d.border, d.fill = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill)
        d.number_format = s.number_format
    ws.row_dimensions[cible].height = ws.row_dimensions[source].height


def etat(xlsx, fichier_reels):
    reels = charger_reels(fichier_reels)
    corr = json.loads(CORRESPONDANCES.read_text())
    connus = set(corr.values())
    s = load_workbook(xlsx)["Statistiques"]
    nouveaux = [r for c, r in reels.items() if c not in connus]
    print(f"{len(nouveaux)} reel(s) absent(s) du suivi :")
    for r in sorted(nouveaux, key=heure_paris):
        print(f"  {code(r)} | {heure_paris(r):%d/%m %H:%M} | {round(r.get('videoDuration') or 0)} s | "
              f"{vues(r)} vues | {r['url']}\n      {(r.get('caption') or '').replace(chr(10), ' ')[:160]}")
    a_relever = []
    for n, c in corr.items():
        r = ligne_du_numero(s, int(n), 7)
        note = (s.cell(r, 13).value or "") if r else ""
        if c in reels and FINAL not in note:
            age = (datetime.now(PARIS).date() - heure_paris(reels[c]).date()).days
            if r is None or age >= 7:
                a_relever.append(f"N°{n} (J+{age})")
    print("Chiffres à relever :", ", ".join(a_relever) or "aucun")


def appliquer(xlsx, sortie, fichier_reels, fichier_plan=None):
    reels = charger_reels(fichier_reels)
    corr = json.loads(CORRESPONDANCES.read_text())
    wb = load_workbook(xlsx)
    p, s = wb["Planning"], wb["Statistiques"]
    aujourdhui = datetime.now(PARIS).date()
    plan = json.loads(Path(fichier_plan).read_text())["publications"] if fichier_plan else []

    publiee = next(r for r in range(p.max_row, 5, -1) if p.cell(r, 11).value == "Publié")
    for pub in plan:
        reel = reels[pub["code"]]
        if pub.get("numero"):
            n = int(pub["numero"])
            r = ligne_du_numero(p, n, 6)
            assert r, f"N°{n} absent du planning"
        else:
            numeros = [p.cell(i, 1).value for i in range(6, p.max_row + 1) if isinstance(p.cell(i, 1).value, int)]
            n = max(numeros) + 1
            r = premiere_ligne_libre(p, 6, (1, 8))
            copier_style(p, publiee, r, range(1, 14))
            p.cell(r, 1).value = n
            p.cell(r, 3).value, p.cell(r, 4).value = JOUR.format(r=r), SEMAINE.format(r=r)
        p.cell(r, 2).value = datetime(*heure_paris(reel).timetuple()[:3])
        p.cell(r, 11).value = "Publié"
        for col, cle in ((5, "serie"), (6, "episode"), (7, "format"), (8, "sujet"), (9, "accroche"),
                         (10, "appel"), (12, "lien"), (13, "notes")):
            if pub.get(cle):
                p.cell(r, col).value = pub[cle]
        corr[str(n)] = pub["code"]
        print(f"N°{n} : {p.cell(r, 8).value} (ligne {r} du planning)")

    modele = next(r for r in range(s.max_row, 6, -1) if isinstance(s.cell(r, 1).value, int))
    for n, c in sorted(corr.items(), key=lambda kv: int(kv[0])):
        if c not in reels:
            continue
        r = ligne_du_numero(s, int(n), 7)
        if r is None:
            r = premiere_ligne_libre(s, 7, (1,))
            copier_style(s, modele, r, range(1, 14))
            s.cell(r, 1).value = int(n)
            for col, f in STATS.items():
                s.cell(r, col).value = f.format(r=r)
        elif FINAL in (s.cell(r, 13).value or ""):
            continue
        reel = reels[c]
        age = (aujourdhui - heure_paris(reel).date()).days
        if 0 < age < 7 and s.cell(r, 5).value not in (None, ""):
            continue  # déjà relevé à la publication : on attend les 7 jours
        s.cell(r, 5).value, s.cell(r, 7).value, s.cell(r, 8).value = vues(reel), reel.get("likesCount"), reel.get("commentsCount")
        if age >= 7:
            s.cell(r, 13).value = f"Vues, j'aime et commentaires relevés le {aujourdhui:%d/%m} sur Instagram (J+{age}) : {FINAL}"
        else:
            s.cell(r, 13).value = (f"Vues, j'aime et commentaires relevés le {aujourdhui:%d/%m} (J+{age}) : "
                                   f"relevé final le {heure_paris(reel).date() + timedelta(days=7):%d/%m}")
        print(f"N°{n} : {vues(reel)} vues, {reel.get('likesCount')} j'aime, {reel.get('commentsCount')} commentaires (J+{age})")

    wb.save(sortie)
    CORRESPONDANCES.write_text(json.dumps(corr, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "etat":
        etat(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 5 and sys.argv[1] == "appliquer":
        appliquer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
    else:
        sys.exit(__doc__)
