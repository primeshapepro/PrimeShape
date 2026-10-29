"""Range le fichier Excel de suivi dans un document JSON, ou l'en ressort, avec contrôle md5.

    python3 veille-reels/suivi_stockage.py empaqueter <suivi.xlsx> <document.json> "<origine>"
    python3 veille-reels/suivi_stockage.py deballer <document.json> <suivi.xlsx>

Le document JSON est celui de la base du catalogue (collection « suivi-excel », document
« courant ») : on l'écrit avec ArtifactData (set, file_path) et on le relit avec ArtifactData
(get, out_dir). Le fichier ne passe ainsi jamais recopié à la main dans la conversation.
"""

import base64
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def empaqueter(xlsx, document, origine):
    data = Path(xlsx).read_bytes()
    Path(document).write_text(json.dumps({
        "nom": "PrimeShape suivi Instagram.xlsx",
        "maj": datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="minutes"),
        "md5": hashlib.md5(data).hexdigest(),
        "taille": len(data),
        "origine": origine,
        "base64": base64.b64encode(data).decode(),
    }))
    print(f"{document} : {len(data)} octets, md5 {hashlib.md5(data).hexdigest()}")


def deballer(document, xlsx):
    doc = json.loads(Path(document).read_text())
    doc = doc["data"] if isinstance(doc.get("data"), dict) else doc
    data = base64.b64decode(doc["base64"])
    if hashlib.md5(data).hexdigest() != doc["md5"]:
        sys.exit("md5 différent : le document est abîmé, ne rien mettre à jour")
    Path(xlsx).write_bytes(data)
    print(f"{xlsx} : version du {doc['maj']} ({doc['origine']}), md5 vérifié")


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "empaqueter":
        empaqueter(*sys.argv[2:])
    elif len(sys.argv) == 4 and sys.argv[1] == "deballer":
        deballer(*sys.argv[2:])
    else:
        sys.exit(__doc__)
