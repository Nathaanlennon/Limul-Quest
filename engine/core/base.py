from os.path import exists

from engine.core.EventSystem import EventSystem
import engine.core.InputSystem as InputSystem
import engine.core.DialogueSystem as DialogueSystem
import engine.core.CombatSystem as CombatSystem
from engine.core.logging_setup import logger
import os
import random
import json



def save_json_with_backup(data, filepath):
    """
    Sauvegarde les données JSON dans `filepath`.
    Si le fichier existe, le renomme en `<filepath>.old`.
    Crée les dossiers manquants si nécessaire.
    """
    # Crée les dossiers si besoin
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Sauvegarde de l'ancien fichier si présent
    if os.path.exists(filepath):
        backup_name = filepath + ".old"
        os.replace(filepath, backup_name)  # remplace l'ancien backup si déjà existant

    # Écriture du nouveau fichier
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {filepath} : {e}")
        return False
    return True

class UniverseData:
    def __init__(self, world, screen_size, name="world", player="hero", player_position = (1,1), **kwargs):
        self.size = screen_size # (rows, cols)
        self.name = name
        self.scenes = {}
        self.current_world = world
        self.player = Player(self, player, self.current_world if self.current_world else "",  player_position)


        self.mode = "exploration"  # Possible modes: : exploration, dialogue and others that are added in extensions
        self.input_system = InputSystem.modes.get(self.mode, InputSystem.exploration_input)

        self.on_mode_change = None
        self.request_text_input = None

        self.dialogue_system = DialogueSystem.DialogueSystem(self)
        self.combat_system = CombatSystem.CombatSystem(self.player)

        self.ext_data = {}
        # extension data
        if charged:
            self.ext_data.update(data_ext.universe_data)

        self.load_save()
        self.set_world(self.current_world)

    # world gestion
    def set_world(self, world, **kwargs):
        if world not in worlds:
            logger.error(f"Monde {world} non trouvé dans les données d'extensions.")
            world_class = World
        else :
            world_class = worlds[world]
        self.add_scene(world, world_class, **kwargs)
        self.current_world = world
        self.player.world = self.scenes[self.current_world]

    def get_scene(self):
        return self.current_world

    def add_scene(self, world_name, scene_class,
                  **kwargs):  # args et kwargs servent à dire qu'on peut mettre autant de paramètres qu'on veut, utile pour le chargement d'une sauvegarde
        if world_name not in self.scenes:
            if scene_class == World:
                self.scenes[world_name] = World(self,"world", "assets/maps/default_map.txt", **kwargs)
            else:
                self.scenes[world_name] = scene_class(self, **kwargs)


    # Mode gestion, mode is the way the sytem and the ui will work, for exemple dialogues and "exploration"
    def mode_change(self, mode):
        self.mode = mode
        self.on_mode_change(mode)
        self.input_system = InputSystem.modes.get(self.mode, InputSystem.exploration_input)

    def set_mode_change_callback(self, callback):
        """L’UI nous donne la fonction à appeler plus tard"""
        self.on_mode_change = callback

    def save_save(self):
        filename = "saves/{}/{}.json".format(self.name, self.name)
        data = {}
        for key, value in self.__dict__.items():
            if key in ("scenes", "current_world", "player", "ext_data", "input_system", "dialogue_system",
                     "combat_system", "on_mode_change", "mode","request_text_input"):
                if key == "scenes":
                    scenes_data = {}
                    for scene_name, scene in value.items():
                        try:
                            scenes_data[scene_name] = scene.extract_data()
                        except Exception as e:
                            logger.error(f"Failed to extract data for scene {scene_name}: {e}")
                    data[key] = scenes_data
                elif key == "current_world":
                    try:
                        data[key] = value
                    except Exception as e:
                        logger.error(f"Failed to save current_world: {e}")
                elif key == "player":
                    try:
                        self.player.save_save()
                    except Exception as e:
                        logger.error(f"Failed to save player {getattr(self.player, 'name', 'unknown')}: {e}")
                elif key == "ext_data":
                    data[key] = {}
                    for ext_k, ext_v in value.items():
                        try:
                            if hasattr(ext_v, "extract_data") and callable(getattr(ext_v, "extract_data")):
                                data[key][ext_k] = ext_v.extract_data()
                            else:
                                data[key][ext_k] = ext_v
                        except Exception as e:
                            logger.error(f"Failed to extract ext_data for {ext_k}: {e}")
                # the rest of the excluded attributes are not saved
            else:
                try:
                    data[key] = value
                except Exception as e:
                    logger.error(f"Failed to save attribute {key}: {e}")
        try:
            if save_json_with_backup(data, filename):
                logger.info(f"Progression de l'univers sauvegardée dans {filename}")
            else:
                logger.error(f"Échec de la sauvegarde de la progression de l'univers dans {filename}")
        except Exception as e:
            logger.error(f"Unexpected error while saving universe to {filename}: {e}")

    def load_save(self):
        filename = "saves/{}/{}.json".format(self.name, self.name)
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    if key == 'scenes':
                        i=0
                        for scene_name, scene_data in value.items():
                            i+=1
                            # Chercher directement dans worlds par le nom de classe
                            if scene_name in worlds:
                                scene_class = worlds[scene_name]
                                self.add_scene(scene_name, scene_class)
                                self.scenes[scene_name].load_data(scene_data)
                            else:
                                logger.warning(f"Classe de scène {scene_name} non trouvée dans worlds.")
                    else:
                        setattr(self, key, value)
            self.player.load_player()
            self.set_world(self.player.world)
            self.player.world = self.scenes[self.current_world]
            logger.info(f"Progression de l'univers chargée depuis {filename}")
        else:
            logger.warning(f"Fichier de sauvegarde introuvable : {filename}")


class World:
    def __init__(self, data, name, map, **kwargs):
        self.data = data
        self.walkable_tiles = ['.', ',', ';', ':', '*', ' ']
        self.entities = {}
        self.name = name
        self.map = map  # empty map for initialisation
        self.event_system = EventSystem(self)

        self.map_data = self.load_map()


    def load_map(self):
        if os.path.exists(self.map) and os.path.isfile(self.map):
            with open(self.map, 'r', encoding='utf-8') as file:
                map_data = [line.rstrip('\n') for line in file]
            return map_data
        else:
            with open("assets/maps/default_map.txt", 'r', encoding='utf-8') as file:
                map_data = [line.rstrip('\n') for line in file]
            logger.warning(f"Fichier de map introuvable : {self.map}, chargement de la map par défaut.")
            return map_data

    def is_walkable(self, tile):
        y, x = tile
        if y < 0 or y >= len(self.map_data) or x < 0 or x >= len(self.map_data[0]):
            return False  # en dehors des limites de la carte
        walkable = False
        if self.map_data[y][x] in self.walkable_tiles:
            if self.event_system.get_event(tile):
                walkable =  self.event_system.get_event(tile).walkable
            else:
                walkable =  True
            # vérifier les entités
            for entity in self.entities.values():
                if tuple(entity.get_position()) == tile and not entity.is_walkable():
                    walkable = False
        return walkable


    def add_entity(self, entity):
        """Add an entity to the world, entity is an instance of Entity class
        it as world, name, position, sprite and other optional parameters
        """
        self.entities[entity.name] = entity
        return entity

    def remove_entity(self, entity_name):
        """Remove an entity from the world by its name"""
        if entity_name in self.entities:
            if self.entities[entity_name].events:
                self.entities[entity_name].remove_all_events()
            del self.entities[entity_name]
    def remove_all_entities(self):
        """Remove all entities from the world"""
        for entity_name in list(self.entities.keys()):
            self.remove_entity(entity_name)


    def extract_data(self):
        """Extract data from the world for saving purposes"""
        data = {
            "map": self.map,
            "entities": {},
            "events": {}
        }
        for name, entity in self.entities.items():
            data["entities"][name] = entity.extract_data()


        return data

    def load_data(self, data):
        """Load data into the world from a saved state"""
        self.map = data.get("map", self.map)
        self.name = data.get("name", self.name)
        entities_data = data.get("entities", {})
        for name, entity_data in entities_data.items():
            self.add_entity(Entity(self, entity_data["name"], entity_data["position"], entity_data["sprite"], walkable=entity_data.get("walkable", False)))


class Entity:
    def __init__(self, world, name, position, sprite, events = None, walkable = False, **kwargs):
        self.name = name
        self.position = position
        self.sprite = sprite
        self.world = world
        self.movable = False
        self.walkable = walkable
        self.events = {}

        if events:
            for event in events:
                self.add_event(event)
                event.entity = self
    def get_position(self):
        return self.position
    def set_position(self, position):
        self.position = position
    def move(self, dx, dy):
        x, y = self.position
        if self.world.is_walkable((x+dx, y+dy)) and self.movable:
            self.position = (x + dx, y + dy)

    def add_event(self, event):
        if not isinstance(event, Event):
            logger.warning(f"Event de type {type(event)} ignoré pour Entité {self.name}") # incorrect type
            return
        self.events[event.name] = event
        event.entity = self
        self.world.event_system.add_event(event)
    def remove_event(self, event_name):
        if event_name in self.events:
            self.world.event_system.remove_event(self.events[event_name])
            del self.events[event_name]
    def remove_all_events(self):
        for event_name in list(self.events.keys()):
            self.remove_event(event_name)
    def is_walkable(self):
        return self.walkable

    def extract_data(self):
        data = {
        }
        for k, v in self.__dict__.items():
            if k not in ("world", "events"):
                data[k] = v

        return data

    def load_data(self, data):
        for key, value in data.items():
            setattr(self, key, value)



class Event:
    def __init__(self, data, world, name, activation_type, action_type, entity=None, position = None, activate = True, **kwargs):
        """
        Initialise un événement dans le jeu.
        :param data: universe data
        :param world: world where the event is located
        :param name: name of the event
        :param activation_type: e.g., "ON_STEP", "ON_INTERACT", "ALWAYS"
        :param action_type: e.g., "MOVE", "DIALOGUE", "COMBAT"
        :param entity: not required, to link the event to an entity
        :param kwargs: additionnal arguments depending on action_type
        ------------------------------------------------------
        Action types and their required arguments:
        - MOVE: target_scene (class), target_position (tuple)
        - DIALOGUE: dialogue (str, path to dialogue file)
        - COMBAT: enemies (list of couples (enemy, proba)), proba (int)
        ------------------------------------------------------
        """
        self.data = data
        self.world = world
        self.name = name
        self.entity = entity  # will be set when added to an entity
        self.position = position #
        self.active = activate
        self.activation_type = activation_type # e.g., "ON_STEP", "ON_INTERACT", "ALWAYS"
        self.walkable = activation_type == "ON_STEP"  # if ON_STEP, the event tile is walkable
        self.action_type = action_type # e.g., "MOVE", "DIALOGUE", "COMBAT", "MODE_CHANGE"
        self.kwargs = kwargs
        self.necessary_args = []

        # vérification que les argumetns nécessaires sont présents selon le type d'action
        if self.action_type == "MOVE":
            self.necessary_args = ["target_scene", "target_position"]
        elif self.action_type == "DIALOGUE":
            self.necessary_args = ["dialogue"]
        elif self.action_type == "COMBAT":
            self.necessary_args = ["enemies", "proba"]# list of enemies and their probabilities ex : [("goblin", 100), ("goblin",50)] | chance to trigger the combat (0-100)
        elif self.action_type=="MODE_CHANGE":
            self.necessary_args = ["mode"] # new mode to switch to
        self.check_event_args(self.necessary_args, kwargs)

    def check_event_args(self, required_args, kwargs):
        missing = [arg for arg in required_args if arg not in kwargs]
        if missing:
            logger.warning(f"Event {self.name} dans {self.world} désactivé : arguments manquants {missing}")
            self.active = False

    @property
    def get_position(self):
        if self.entity is None:
            return None
        return self.entity.get_position()

    def is_facing_player(self):
        x, y = self.data.player.get_position()
        dx, dy = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}.get(
            self.data.player.orientation, (0, 0)
        )
        return (x + dx, y + dy) == self.get_position


    # activation stuff
    def activation(self):
        if self.active:
            if self.action_type == "MOVE":
                self.data.set_world(self.kwargs["target_scene"])
                self.data.player.set_position(self.kwargs["target_position"])
            elif self.action_type == "DIALOGUE":
                self.data.mode_change("dialogue")
                self.data.dialogue_system.set_dialogues(self.kwargs["dialogue"])
            elif self.action_type == "COMBAT":
                if random.random() <= self.kwargs["proba"]:
                    self.data.mode_change("combat")
                    for (enemy, proba) in self.kwargs["enemies"]:
                        if random.random() <= proba:
                            self.data.combat_system.add_fighter(enemy)
            elif self.action_type == "MODE_CHANGE":
                self.data.mode_change(self.kwargs["mode"])


    def should_trigger(self, action):
        if self.activation_type == "ON_STEP":
            return self.data.player.get_position() == self.get_position
        elif self.activation_type == "ON_INTERACT":
            return self.is_facing_player() and action == "INTERACT"
        elif self.activation_type == "ALWAYS":
            return action in ["UP", "DOWN", "LEFT", "RIGHT"]
        return False

    def extract_data(self):
        data = {
            "name": self.name,
            "position": self.position,
            "active": self.active,
            "activation_type": self.activation_type,
            "action_type": self.action_type,
            "kwargs": self.kwargs,
            "entity": self.entity.name if self.entity else None
        }
        return data



class NPC(Entity):
    def __init__(self, world, name, position, sprite, dialogue="assets/dialogues/default_dialogue.json", **kwargs):
        super().__init__(world, name, position, sprite)
        self.dialogue = dialogue

        self.add_event(
            Event(
                world.data, self.world,
                f"dialogue_event_{name}",
                "ON_INTERACT",
                "DIALOGUE",
                self,
                dialogue=self.dialogue
        ))






class Player(Entity):
    def __init__(self,universe, name, world, position):
        super().__init__(world, name, position, '@')
        self.movable = True
        self.universe = universe

        self.orientation = "DOWN"  # Possible orientations: UP, DOWN, LEFT, RIGHT

        self.inventory = { # dictionnary, id of the item is the key, the value is the quantity

        }
        self.ext_data = {
            "abilities": {}
        }
        if charged:
            self.ext_data.update(data_ext.player_data)
        # combat stats
        self.max_hp = 100
        self.hp = self.max_hp
        self.damage = 10
        self.defense = 5

    def attack(self):
            return self.damage



    def facing_position(self): # gives the tiles facing the player
        x, y = self.get_position()
        dx, dy = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}.get(
            self.orientation, (0, 0)
        )
        return x + dx, y + dy

    def add_to_inventory(self, item_id, quantity=1):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def remove_from_inventory(self, item_id, quantity=1):
        if item_id in self.inventory and self.inventory[item_id] >= quantity:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]

    def death(self):
        """Gère la mort du joueur. À implémenter."""
        logger.info("Le joueur est mort")


    def save_save(self):
        filename = "saves/{}/{}/{}.json".format(self.universe.name,self.name, self.name)
        # Crée un dictionnaire filtré pour la sauvegarde
        data = {k: v for k, v in self.__dict__.items() if k not in ("world", "events", "universe")}
        data['world'] = self.world.name

        if save_json_with_backup(data, filename):
            logger.info(f"Progression du joueur sauvegardée dans {filename}")
        else:
            logger.error(f"Échec de la sauvegarde de la progression du joueur dans {filename}")

    def load_player(self):
        filename = "saves/{}/{}/{}.json".format(self.universe.name,self.name, self.name)
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    setattr(self, key, value)
            logger.info(f"Progression du joueur chargée depuis {filename}")
        else:
            logger.warning(f"Fichier de sauvegarde introuvable : {filename} (normal if new player)")


"""Charge les items depuis un fichier JSON. Retourne un dict vide si le fichier est absent ou invalide."""
if os.path.exists("extensions/data_extensions.py") and os.path.isfile("extensions/data_extensions.py"):
    import extensions.data_extensions as data_ext
    charged = True

else:
    logger.warning(f"Fichier de data introuvable : {'extensions.data_extensions.py'}, les extensions de data ne seront pas chargées. Executez setup_environment.py qui est dans l'engine pour utiliser.")
    charged = False

if charged:
    worlds = data_ext.worlds
else:
    worlds = {}

