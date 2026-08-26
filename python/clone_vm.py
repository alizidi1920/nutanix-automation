"""
clone_vm.py
-----------
Clone une VM existante sur le cluster Nutanix via l'API REST v2.

Usage :
    python3 clone_vm.py --source "RHEL9-Golden-Final" --clone "Linux-Clone01"

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

import argparse
from nutanix_api import get_vm_uuid, get_vm_by_name, post, print_separator


def clone_vm(source_name, clone_name, ram_mb=None, vcpu=None):
    """
    Clone une VM source vers un nouveau nom.

    Paramètres :
        source_name : nom de la VM source (ex: RHEL9-Golden-Final)
        clone_name  : nom du clone à créer
        ram_mb      : RAM du clone en MB (reprend celle de la source si None)
        vcpu        : vCPU du clone (reprend ceux de la source si None)
    """
    print_separator(f"Clonage : {source_name}  →  {clone_name}")

    # Récupération des infos de la VM source
    source_vm = get_vm_by_name(source_name)
    if not source_vm:
        raise ValueError(f"VM source '{source_name}' introuvable.")

    source_uuid = source_vm.get("uuid")
    source_ram  = ram_mb  if ram_mb else source_vm.get("memory_mb", 2048)
    source_vcpu = vcpu    if vcpu   else source_vm.get("num_vcpus", 2)

    print(f"  Source UUID : {source_uuid}")
    print(f"  Clone RAM   : {source_ram} MB")
    print(f"  Clone vCPU  : {source_vcpu}")

    payload = {
        "spec_list": [
            {
                "name": clone_name,
                "memory_mb": source_ram,
                "num_vcpus": source_vcpu,
                "num_cores_per_vcpu": source_vm.get("num_cores_per_vcpu", 1),
                "override_network_config": False
            }
        ]
    }

    result = post(f"vms/{source_uuid}/clone", payload)
    task_uuid = result.get("task_uuid", "N/A")

    print(f"  ✅ Clone '{clone_name}' créé avec succès.")
    print(f"  Task UUID : {task_uuid}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloner une VM sur Nutanix CE")
    parser.add_argument("--source", required=True, help="Nom de la VM source")
    parser.add_argument("--clone",  required=True, help="Nom du clone à créer")
    parser.add_argument("--ram",    type=int, default=None, help="RAM en MB (optionnel)")
    parser.add_argument("--vcpu",   type=int, default=None, help="Nombre de vCPU (optionnel)")
    args = parser.parse_args()

    try:
        clone_vm(args.source, args.clone, args.ram, args.vcpu)
    except Exception as e:
        print(f"❌ Erreur : {e}")
