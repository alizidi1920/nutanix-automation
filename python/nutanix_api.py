"""
nutanix_api.py
--------------
Fonctions réutilisables pour communiquer avec l'API REST Nutanix.
Toutes les autres scripts importent ce module.

Auteur  : Ali Zidi — Stagiaire Ooredoo Tunisie
Projet  : Phase 6 — Automatisation
"""

import requests
import base64
import json
import urllib3

# ── Désactiver les warnings SSL (certificat auto-signé en lab) ──────────────
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Configuration de l'environnement ────────────────────────────────────────
PRISM_HOST     = "192.168.159.21"
PRISM_PORT     = 9440
PRISM_USER     = "****"
PRISM_PASSWORD = "******"          # à adapter selon ton environnement

BASE_URL_V2 = f"https://{PRISM_HOST}:{PRISM_PORT}/api/nutanix/v2.0"
BASE_URL_V3 = f"https://{PRISM_HOST}:{PRISM_PORT}/api/nutanix/v3"


# ── Construction des headers d'authentification ──────────────────────────────
def get_headers():
    """Retourne les headers HTTP avec Basic Auth encodé en Base64."""
    credentials = f"{PRISM_USER}:{PRISM_PASSWORD}"
    encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encoded}"
    }


# ── Requêtes HTTP génériques ─────────────────────────────────────────────────
def get(endpoint, version="v2"):
    """Effectue une requête GET sur l'API Nutanix."""
    base = BASE_URL_V2 if version == "v2" else BASE_URL_V3
    url = f"{base}/{endpoint}"
    response = requests.get(url, headers=get_headers(), verify=False)
    response.raise_for_status()
    return response.json()


def post(endpoint, payload, version="v2"):
    """Effectue une requête POST sur l'API Nutanix."""
    base = BASE_URL_V2 if version == "v2" else BASE_URL_V3
    url = f"{base}/{endpoint}"
    response = requests.post(url, headers=get_headers(),
                             data=json.dumps(payload), verify=False)
    response.raise_for_status()
    return response.json()


def delete(endpoint, version="v2"):
    """Effectue une requête DELETE sur l'API Nutanix."""
    base = BASE_URL_V2 if version == "v2" else BASE_URL_V3
    url = f"{base}/{endpoint}"
    response = requests.delete(url, headers=get_headers(), verify=False)
    response.raise_for_status()
    return response.status_code


# ── Fonctions utilitaires ────────────────────────────────────────────────────
def get_all_vms():
    """Retourne la liste complète des VMs (entities)."""
    data = get("vms")
    return data.get("entities", [])


def get_vm_by_name(name):
    """Recherche une VM par son nom. Retourne l'entité ou None."""
    vms = get_all_vms()
    for vm in vms:
        if vm.get("name") == name:
            return vm
    return None


def get_vm_uuid(name):
    """Retourne l'UUID d'une VM à partir de son nom."""
    vm = get_vm_by_name(name)
    if vm:
        return vm.get("uuid")
    raise ValueError(f"VM '{name}' introuvable.")


def get_cluster_uuid():
    """Retourne l'UUID du cluster."""
    data = get("clusters")
    entities = data.get("entities", [])
    if entities:
        return entities[0].get("uuid")
    raise ValueError("Aucun cluster trouvé.")


def get_network_uuid():
    """Retourne l'UUID du premier réseau disponible."""
    data = get("networks")
    entities = data.get("entities", [])
    if entities:
        return entities[0].get("uuid")
    raise ValueError("Aucun réseau trouvé.")


def print_separator(title=""):
    """Affiche une ligne de séparation dans la console."""
    print("\n" + "─" * 60)
    if title:
        print(f"  {title}")
        print("─" * 60)


if __name__ == "__main__":
    print_separator("Test de connexion à Prism Element")
    try:
        vms = get_all_vms()
        print(f"✅ Connexion OK — {len(vms)} VM(s) trouvée(s)")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
