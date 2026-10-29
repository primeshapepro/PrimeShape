# Suivi Instagram : mise à jour à chaque publication

Le fichier Excel de suivi d'Andy (Tableau de bord, Planning, Stories, Statistiques,
Séries & idées, Routine & checklist) est mis à jour par Claude dès qu'une vidéo
paraît sur @primeshapefr. Ce dossier est public : aucun chiffre ni contenu du
fichier n'y est versionné, seulement les scripts et la correspondance
« numéro du planning -> code du reel » (`suivi-correspondances.json`), qui ne
contient que des liens publics.

## Où vit le fichier

- **Version de référence :** base du catalogue
  (https://claude.ai/artifact/QyyrrDEwYMtQdhEnSLV5wz), collection `suivi-excel`,
  document `courant`, privée comme le catalogue. `suivi_stockage.py` l'empaquette
  et la déballe avec contrôle md5.
- **Andy reçoit chaque nouvelle version dans la conversation** (SendUserFile).
  S'il modifie le fichier et le renvoie, sa version devient la référence :
  l'empaqueter et l'écrire dans `courant` avant toute autre mise à jour.
- **Pas de Google Drive :** le connecteur ne transfère un fichier binaire qu'en
  base64 recopié dans la conversation, ce qui s'est révélé peu fiable pour un
  fichier de 40 Ko (essai raté le 29/10/2026).

## Chaque soir (tâche programmée, 21 h 40 heure de Paris)

1. Se mettre sur la branche `claude/vigilant-cannon-mgk68t`.
2. Relever le compte : `apify~instagram-reel-scraper`, `username: ["primeshapefr"]`,
   `resultsLimit: 10`, résultats bruts dans un `reels.json` (environ 0,03 $).
3. Récupérer la référence : ArtifactData `get` de `suivi-excel/courant` avec
   `out_dir`, puis `python3 veille-reels/suivi_stockage.py deballer <json> <xlsx>`.
4. `python3 veille-reels/suivi.py etat <xlsx> <reels.json>` : reels absents du
   suivi et chiffres à relever.
5. S'il n'y a rien à faire, s'arrêter là : une ligne, pas de fichier envoyé.
6. Pour chaque nouveau reel, le regarder (premières images, légende, son), puis :
   - s'il réalise une idée déjà au planning (même sujet), reprendre son numéro ;
     sinon, nouvelle ligne ;
   - remplir série et format avec les valeurs des listes du fichier ; épisode
     « Bonus » s'il est hors série (ne jamais renuméroter les épisodes prévus) ;
   - accroche = texte à l'écran des 2 premières secondes ; appel à l'action « — »
     s'il n'y en a pas ; lien = adresse Instagram ou fichier de montage ; notes =
     date et heure de publication (heure de Paris) et musique.

   Écrire tout ça dans un `plan.json` (format dans `suivi.py`).
7. `python3 veille-reels/suivi.py appliquer <xlsx> <sortie.xlsx> <reels.json> [plan.json]`,
   puis recalculer avec LibreOffice (skill xlsx, `scripts/recalc.py`) :
   0 erreur exigée.
8. `suivi_stockage.py empaqueter`, écrire dans `suivi-excel/courant`
   (ArtifactData `set`, `file_path`, `if_version`), relire et redéballer pour
   vérifier le md5.
9. Commit et push de `suivi-correspondances.json`.
10. Envoyer le fichier à Andy (SendUserFile, `status: proactive`) avec un message
    court : ce qui a été ajouté, les chiffres relevés, et ce qu'il reste à
    remplir lui-même (comptes touchés, partages, enregistrements, nouveaux
    abonnés, visibles seulement dans ses statistiques Instagram).

## Ce que Claude ne touche pas

Les colonnes qu'Andy remplit (comptes touchés, partages, enregistrements,
nouveaux abonnés, abonnés du lundi), l'onglet Stories, Séries & idées et
Routine & checklist. Les chiffres relevés par Claude (vues, j'aime,
commentaires) le sont à la publication puis une dernière fois à 7 jours ;
une note contenant « relevé final » ne bouge plus.
