from engine.core.logging_setup import logger
import os
import json
import random


def load_enemies_list(file_path="assets/enemies/enemies.json"):
    """Charge les combattants depuis un fichier JSON. Retourne une liste vide si le fichier est absent ou invalide."""
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Erreur lors du chargement de {file_path} : {e}")
            return {}
    else:
        logger.warning(f"Fichier de combattants introuvable : {file_path}")
        return {}


def attack_target(attacker, target):
    """Effectue une attaque basique sur la cible."""
    attack_value = attacker.attack
    damage = random.randint(attack_value - 2, attack_value + 2)
    target.receive_damage(damage)


def receive_damage(target, damage):
    """Réduit les points de vie de l'ennemi."""
    target.hp -= damage - target.defense
    if target.hp <= 0:
        target.death()


class CombatSystem:
    def __init__(self, player):
        self.player = player
        self.enemies_list = load_enemies_list()
        self.fighters = []
        self.loot = []

    class Enemy:
        def __init__(self, combat_system, enemy_data):
            self.name = enemy_data.get("name", "Ennemi inconnu")
            self.attacks = enemy_data.get("attacks", [])
            self.attack = enemy_data.get("attack", 0)
            self.defense = enemy_data.get("defense", 0)
            self.hp = enemy_data.get("hp", 10)
            self.loot = enemy_data.get("loot", [])

            self.combat_system = combat_system

        def loot(self):
            if self.hp <= 0:
                for item, proba in self.loot:
                    if random.randint(1, 100) <= proba * 100:
                        self.combat_system.loot.append((item, 1))

        def death(self):
            """Gère la mort de l'ennemi."""
            self.loot()
            self.combat_system.remove_fighter(self)


    def add_fighter(self, fighter):
        """Ajoute un combattant à la liste des combattants en fonction de son ID.

            Args:
                fighter (str): L'ID du combattant à ajouter.
        """
        if fighter in self.enemies_list:
            self.fighters.append(self.Enemy(self, self.enemies_list[fighter]))

    def remove_fighter(self, fighter):
        """Retire un combattant de la liste des combattants.

            Args:
                fighter (Enemy): L'instance du combattant à retirer.
        """
        if fighter in self.fighters:
            self.fighters.remove(fighter)

    def give_loot(self):
        """Donne le loot au joueur après le combat."""
        for item_id, quantity in self.loot:
            self.player.add_to_inventory(item_id, quantity)
        self.loot = []

    def player_turn(self):
        """Effectue le tour du joueur."""
        # Pour l'instant, le joueur attaque le premier ennemi dans la liste
        if self.fighters:
            attack_target(self.player, self.fighters[0])

    def combat_round(self):
        """Effectue un round de combat où chaque combattant attaque."""
        self.player_turn()
        for fighter in self.fighters:
            attack_target(fighter, self.player)

