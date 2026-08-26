"""
snapshot.py
-----------
Crée un snapshot d'une VM sur le cluster Nutanix via l'API REST v2.

Usage :
    python3 snapshot.py --name "Linux-App01" --snapshot "snap-2026-08-19"

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

import argparse
from datetime import datetime
from nutanix_api import get_vm_uuid, post, print_separator


def create_snapshot(vm_name, snapshot_name=None):
    """
    Crée un snapshot pour la VM spécifiée.

    Paramètres :
        vm_name       : nom de la VM source
        snapshot_name : nom du snapshot (auto-généré si non fourni)
    """
    print_separator(f"Snapshot de la VM : {vm_name}")

    uuid = get_vm_uuid(vm_name)
    print(f"  UUID de la VM : {uuid}")

    # Nom automatique si non fourni
    if not snapshot_name:
        snapshot_name = f"snap-{vm_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    payload = {
        "snapshot_specs": [
            {
                "vm_uuid": uuid,
                "snapshot_name": snapshot_name
            }
        ]
    }

    result = post("snapshots", payload)
    task_uuid = result.get("task_uuid", "N/A")

    print(f"  ✅ Snapshot '{snapshot_name}' créé avec succès.")
    print(f"  Task UUID : {task_uuid}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Créer un snapshot sur Nutanix CE")
    parser.add_argument("--name",     required=True, help="Nom de la VM source")
    parser.add_argument("--snapshot", default=None,  help="Nom du snapshot (optionnel)")
    args = parser.parse_args()

    try:
        create_snapshot(args.name, args.snapshot)
    except Exception as e:
        print(f"❌ Erreur : {e}")
