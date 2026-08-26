"""
delete_vm.py
------------
Supprime une VM du cluster Nutanix via l'API REST v2.

Usage :
    python3 delete_vm.py --name "Linux-New01"

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

import argparse
from nutanix_api import get_vm_uuid, delete, print_separator


def delete_vm(name):
    """
    Supprime une VM par son nom.

    Paramètres :
        name : nom de la VM à supprimer
    """
    print_separator(f"Suppression de la VM : {name}")

    uuid = get_vm_uuid(name)
    print(f"  UUID trouvé : {uuid}")

    # Confirmation avant suppression
    confirm = input(f"  ⚠️  Confirmer la suppression de '{name}' ? (oui/non) : ")
    if confirm.strip().lower() != "oui":
        print("  ❌ Suppression annulée.")
        return

    status_code = delete(f"vms/{uuid}")

    if status_code in (200, 201, 204):
        print(f"  ✅ VM '{name}' supprimée avec succès (HTTP {status_code}).")
    else:
        print(f"  ⚠️  Réponse inattendue : HTTP {status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Supprimer une VM sur Nutanix CE")
    parser.add_argument("--name", required=True, help="Nom de la VM à supprimer")
    args = parser.parse_args()

    try:
        delete_vm(args.name)
    except Exception as e:
        print(f"❌ Erreur : {e}")
