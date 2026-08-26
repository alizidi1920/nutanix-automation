"""
create_vm.py
------------
Crée une nouvelle VM sur le cluster Nutanix via l'API REST v2.

Usage :
    python3 create_vm.py --name "Linux-New01" --ram 2048 --vcpu 2

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

import argparse
from nutanix_api import post, get_network_uuid, print_separator


def create_vm(name, ram_mb=2048, vcpu=2, cores_per_vcpu=1):
    """
    Crée une VM avec les paramètres spécifiés.

    Paramètres :
        name            : nom de la VM
        ram_mb          : RAM en mégaoctets (défaut : 2048)
        vcpu            : nombre de vCPU (défaut : 2)
        cores_per_vcpu  : cœurs par vCPU (défaut : 1)
    """
    print_separator(f"Création de la VM : {name}")

    network_uuid = get_network_uuid()
    print(f"  Réseau détecté : {network_uuid}")

    payload = {
        "name": name,
        "memory_mb": ram_mb,
        "num_vcpus": vcpu,
        "num_cores_per_vcpu": cores_per_vcpu,
        "power_state": "off",
        "vm_disks": [
            {
                "is_cdrom": False,
                "disk_address": {
                    "device_bus": "scsi",
                    "device_index": 0
                },
                "vm_disk_create": {
                    "storage_container_uuid": "",   # laissé vide = container par défaut
                    "size": 32212254720             # 30 Go en octets
                }
            }
        ],
        "vm_nics": [
            {
                "network_uuid": network_uuid,
                "is_connected": True
            }
        ]
    }

    result = post("vms", payload)
    task_uuid = result.get("task_uuid", "N/A")

    print(f"  ✅ VM '{name}' créée avec succès.")
    print(f"  Task UUID : {task_uuid}")
    print(f"  RAM       : {ram_mb} MB")
    print(f"  vCPU      : {vcpu}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Créer une VM sur Nutanix CE")
    parser.add_argument("--name",  required=True,       help="Nom de la VM")
    parser.add_argument("--ram",   type=int, default=2048, help="RAM en MB (défaut: 2048)")
    parser.add_argument("--vcpu",  type=int, default=2,    help="Nombre de vCPU (défaut: 2)")
    args = parser.parse_args()

    try:
        create_vm(args.name, args.ram, args.vcpu)
    except Exception as e:
        print(f"❌ Erreur : {e}")
