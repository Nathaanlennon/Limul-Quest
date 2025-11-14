from engine.core.logging_setup import logger
import os
import json

def load_items(file_path="assets/items/items.json"):
    """Charge les items depuis un fichier JSON. Retourne un dict vide si le fichier est absent ou invalide."""
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Erreur lors du chargement de {file_path} : {e}")
            return {}
    else:
        logger.warning(f"Fichier d'items introuvable : {file_path}")
        return {}


items = load_items()

def get_item(item) -> dict:
    """Récupère un item par son ID. Retourne un placeholder si absent et log l'erreur."""
    if item not in items:
        logger.warning(f"Item '{item}' introuvable dans la base de données d'items.")
        return {
            "name": "Objet inconnu",
            "description": "Cet objet n'existe pas ou n'est pas encore défini.",
        }
    return items[item]

