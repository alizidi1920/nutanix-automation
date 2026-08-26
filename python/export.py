"""
export.py
---------
Exporte l'inventaire complet des VMs en JSON et CSV
dans le dossier ../exports/

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

import json
import csv
import os
from datetime import datetime
from nutanix_api import get_all_vms, print_separator

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")


def export_json(vms):
    """Exporte la liste des VMs au format JSON."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, "inventaire_vms.json")

    export_data = {
        "date_export": datetime.now().isoformat(),
        "cluster": "NTNX-512e1bdd-A",
        "prism_element": "192.168.159.21:9440",
        "total_vms": len(vms),
        "vms": []
    }

    for vm in vms:
        nics = vm.get("vm_nics", [])
        ip = nics[0].get("ip_address", "N/A") if nics else "N/A"
        export_data["vms"].append({
            "name":        vm.get("name", "N/A"),
            "uuid":        vm.get("uuid", "N/A"),
            "power_state": vm.get("power_state", "N/A"),
            "memory_mb":   vm.get("memory_mb", "N/A"),
            "num_vcpus":   vm.get("num_vcpus", "N/A"),
            "ip_address":  ip,
            "host_uuid":   vm.get("host_uuid", "N/A"),
            "description": vm.get("description", "")
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Export JSON : {os.path.abspath(path)}")
    return path


def export_csv(vms):
    """Exporte la liste des VMs au format CSV."""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, "inventaire_vms.csv")

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        # En-tête
        writer.writerow(["Nom", "UUID", "Power State", "RAM (MB)",
                         "vCPU", "IP", "Host UUID", "Description"])
        # Données
        for vm in vms:
            nics = vm.get("vm_nics", [])
            ip = nics[0].get("ip_address", "N/A") if nics else "N/A"
            writer.writerow([
                vm.get("name", "N/A"),
                vm.get("uuid", "N/A"),
                vm.get("power_state", "N/A"),
                vm.get("memory_mb", "N/A"),
                vm.get("num_vcpus", "N/A"),
                ip,
                vm.get("host_uuid", "N/A"),
                vm.get("description", "")
            ])

    print(f"  ✅ Export CSV  : {os.path.abspath(path)}")
    return path


if __name__ == "__main__":
    print_separator("Export de l'inventaire des VMs")
    try:
        vms = get_all_vms()
        print(f"  {len(vms)} VM(s) récupérée(s).\n")
        export_json(vms)
        export_csv(vms)
        print(f"\n  Export terminé — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    except Exception as e:
        print(f"❌ Erreur : {e}")
