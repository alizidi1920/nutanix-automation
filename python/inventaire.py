"""
inventaire.py
-------------
Liste toutes les VMs du cluster Nutanix avec leurs informations détaillées.

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

from nutanix_api import get_all_vms, print_separator


def afficher_inventaire():
    """Affiche l'inventaire complet des VMs dans la console."""
    print_separator("Inventaire des VMs — Cluster Nutanix CE")

    vms = get_all_vms()

    if not vms:
        print("Aucune VM trouvée.")
        return

    # En-tête du tableau
    print(f"{'N°':<4} {'Nom':<25} {'UUID':<38} {'Power':<10} {'RAM (MB)':<10} {'vCPU':<6} {'IP'}")
    print("-" * 110)

    for i, vm in enumerate(vms, start=1):
        nom        = vm.get("name", "N/A")
        uuid       = vm.get("uuid", "N/A")
        power      = vm.get("power_state", "N/A")
        ram        = vm.get("memory_mb", "N/A")
        vcpu       = vm.get("num_vcpus", "N/A")

        # Récupération de l'adresse IP (si disponible)
        nics = vm.get("vm_nics", [])
        ip = nics[0].get("ip_address", "N/A") if nics else "N/A"

        print(f"{i:<4} {nom:<25} {uuid:<38} {power:<10} {ram:<10} {vcpu:<6} {ip}")

    print("-" * 110)
    print(f"Total : {len(vms)} VM(s)\n")


if __name__ == "__main__":
    try:
        afficher_inventaire()
    except Exception as e:
        print(f"❌ Erreur : {e}")
