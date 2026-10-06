# nutanix-automation

## Présentation

Ce projet regroupe l'ensemble des scripts d'automatisation développés dans le cadre du stage
**"Conception, déploiement et évaluation d'une infrastructure Nutanix Community Edition"**


Il couvre la **Phase** du : automatisation des opérations d'administration
via l'API REST Nutanix et les playbooks Ansible.

---

## Environnement

| Élément            | Valeur                          |
|--------------------|---------------------------------|
| Prism Element      | https://192.168.159.21:9440     |
| Hôte AHV           | NTNX-512e1bdd-A — 192.168.159.20|
| Cluster            | Single Node                     |
| Utilisateur API    | admin                           |
| Protocole          | HTTPS / REST (Basic Auth)       |

---

## Structure du projet

```
nutanix-automation/
├── README.md
├── python/
│   ├── nutanix_api.py     ← fonctions réutilisables (base)
│   ├── inventaire.py      ← liste toutes les VMs
│   ├── create_vm.py       ← créer une VM
│   ├── delete_vm.py       ← supprimer une VM
│   ├── snapshot.py        ← créer un snapshot
│   ├── clone_vm.py        ← cloner une VM
│   └── export.py          ← exporter inventaire JSON/CSV
├── ansible/
│   ├── inventory.yml      ← hôtes Ansible
│   ├── vars/nutanix.yml   ← variables (IP, credentials)
│   └── playbooks/
│       ├── create_vm.yml
│       ├── delete_vm.yml
│       ├── snapshot.yml
│       ├── clone_vm.yml
│       ├── power_on.yml
│       ├── power_off.yml
│       └── inventaire.yml
└── exports/
    ├── inventaire_vms.json
    └── inventaire_vms.csv
```

---

## Prérequis

### Python
```bash
pip install requests urllib3
```

### Ansible
```bash
pip install ansible
ansible-galaxy collection install nutanix.ncp
```

---

## Utilisation rapide — Python

```bash
cd python/

# Lister toutes les VMs
python3 inventaire.py

# Créer une VM
python3 create_vm.py --name "Linux-New01" --ram 2048 --vcpu 2

# Supprimer une VM
python3 delete_vm.py --name "Linux-New01"

# Créer un snapshot
python3 snapshot.py --name "Linux-App01" --snapshot "snap-$(date +%F)"

# Cloner une VM
python3 clone_vm.py --source "RHEL9-Golden-Final" --clone "Linux-Clone01"

# Exporter l'inventaire
python3 export.py
```

---

## Utilisation rapide — Ansible

```bash
cd ansible/

# Inventaire
ansible-playbook -i inventory.yml playbooks/inventaire.yml

# Créer une VM
ansible-playbook -i inventory.yml playbooks/create_vm.yml

# Démarrer une VM
ansible-playbook -i inventory.yml playbooks/power_on.yml -e "vm_name=Linux-App01"

# Arrêter une VM
ansible-playbook -i inventory.yml playbooks/power_off.yml -e "vm_name=Linux-App01"

# Snapshot
ansible-playbook -i inventory.yml playbooks/snapshot.yml -e "vm_name=Linux-App01"

# Cloner
ansible-playbook -i inventory.yml playbooks/clone_vm.yml

# Supprimer
ansible-playbook -i inventory.yml playbooks/delete_vm.yml -e "vm_name=Linux-Clone01"
```

---

## Stagiaire

**Ali Zidi** — Stagiaire Cloud / DevSecOps  
ESPRIT Tunis — ArcTIC / DevSecOps  

