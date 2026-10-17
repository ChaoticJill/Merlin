"""
Remise à zéro de Merlin avant la mise en production.

Supprime toutes les saisines, toutes les fiches collectivités (et leurs agents), tous les
thèmes et tous les textes applicables (descripteurs). Les fichiers actuels sont d'abord déplacés dans un dossier de
sauvegarde horodaté, pour pouvoir les récupérer en cas d'erreur.

Utilisation :
  1. Arrêter l'application Merlin (Ctrl+C dans le terminal).
  2. Placer ce fichier dans le même dossier que merlin_app.py.
  3. Lancer :  python reset_merlin.py
  4. Relancer l'application :  streamlit run merlin_app.py
     (les fichiers vides sont recréés automatiquement au démarrage)

Les comptes utilisateurs ne sont PAS touchés.
"""
import os
import shutil
from datetime import datetime

FICHIERS_A_REINITIALISER = [
    "merlin_saisines.csv",   # toutes les saisines
    "merlin_collectivites.json",  # fiches collectivités et agents
    "merlin_themes.json",    # thèmes / descripteurs
    "merlin_textes.json",    # textes applicables
]

presents = [f for f in FICHIERS_A_REINITIALISER if os.path.exists(f)]

if not presents:
    print("Aucun fichier à réinitialiser dans ce dossier. Rien n'a été modifié.")
    raise SystemExit

print("Les fichiers suivants vont être mis de côté (puis recréés vides) :")
for f in presents:
    print(f"  - {f}")

if input("Confirmer ? (oui/non) : ").strip().lower() not in ("oui", "o", "yes", "y"):
    print("Annulé. Rien n'a été modifié.")
    raise SystemExit

dossier = "sauvegarde_test_" + datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(dossier)
for f in presents:
    shutil.move(f, os.path.join(dossier, f))

print(f"Terminé. Anciennes données sauvegardées dans : {dossier}/")
print("Relancez l'application : les fichiers vides seront recréés automatiquement.")
