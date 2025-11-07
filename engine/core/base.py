from os.path import exists

from engine.core.EventSystem import EventSystem
import engine.core.InputSystem as InputSystem
import engine.core.DialogueSystem as DialogueSystem
from engine.core.logging_setup import logger
import os

"""Charge les items depuis un fichier JSON. Retourne un dict vide si le fichier est absent ou invalide."""
if os.path.exists("extensions/data_extensions.py") and os.path.isfile("extensions/data_extensions.py"):
    import extensions.data_extensions as data_ext
    charged = True

else:
    logger.warning(f"Fichier de data introuvable : {'extensions.data_extensions.py'}, les extensions de data ne seront pas chargées. Importez scripts/setup_environment.py dans le main pour utiliser.")
    charged = False


class UniverseData:
    def __init__(self, scene, screen_size, **kwargs):
        self.size = screen_size # (rows, cols)
        self.scenes = {}
        self.current_scene = None
        self.player = Player(self.current_scene, self.current_scene.spawn_player if self.current_scene else (2, 2))
        self.set_scene(scene)

        self.mode = "exploration"  # Possible modes: : exploration, dialogue and others that are added in extensions
        self.input_system = InputSystem.modes.get(self.mode, InputSystem.exploration_input)
        # self.input_systems = {modes
        #     "exploration" : InputSystem(self)
        # }
        self.on_mode_change = None

        self.dialogue_system = DialogueSystem.DialogueSystem(self)

        # extension data
        if charged:
            self.ext_data = data_ext.universe_data

    # scene gestion
    def set_scene(self, scene_class, **kwargs):
        self.add_scene(scene_class, **kwargs)
        self.current_scene = self.scenes[scene_class]
        self.player.position = self.current_scene.spawn_player
        self.player.world = self.current_scene

    def get_scene(self):
        return self.current_scene

    def add_scene(self, scene_class,
                  **kwargs):  # args et kwargs servent à dire qu'on peut mettre autant de paramètres qu'on veut, utile pour le chargement d'une sauvegarde
        if scene_class not in self.scenes:
            self.scenes[scene_class] = scene_class(self, **kwargs)


    # Mode gestion, mode is the way the sytem and the ui will work, for exemple dialogues and "exploration"
    def mode_change(self, mode):
        self.mode = mode
        self.on_mode_change(mode)
        if mode == "exploration":
            self.input_system = InputSystem.exploration_input
        elif mode == "dialogue":
            self.input_system = InputSystem.dialogue_input
        elif mode == "inventory":
            self.input_system = InputSystem.inventory_input

    def set_mode_change_callback(self, callback):
        """L’UI nous donne la fonction à appeler plus tard"""
        self.on_mode_change = callback


    def load_save(self):
        ...  # Implémentation du chargement de sauvegarde à venir


class World:
    def __init__(self, data, map, spawn_player, **kwargs):
        self.data = data
        self.walkable_tiles = ['.', ',', ';', ':', '*', ' ']
        self.entities = {}
        self.map = map  # empty map for initialisation
        self.spawn_player = spawn_player  # Default spawn position for player
        self.event_system = EventSystem(self)

        self.map_data = self.load_map()


    def load_map(self):
        with open(self.map, 'r') as file:
            map_data = [line.rstrip('\n') for line in file]
        return map_data

    def is_walkable(self, tile):
        x, y = tile
        if self.map_data[x][y] in self.walkable_tiles:
            if self.event_system.get_event(tile):
                return self.event_system.get_event(tile).walkable
            else:
                return True
        return False


    def add_entity(self, entity):
        """Add an entity to the world, entity is an instance of Entity class
        it as world, name, position, sprite and other optional parameters
        """
        self.entities[entity.name] = entity
        return entity



class Entity:
    def __init__(self, world, name, position, sprite, events = None, **kwargs):
        self.name = name
        self.position = position
        self.sprite = sprite
        self.world = world
        self.movable = False
        self.events = {}

        if events:
            for event in events:
                self.add_event(event)
                event.entity = self

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


class Event:
    def __init__(self, data, world, name, activation_type, action_type, entity=None, **kwargs):
        self.data = data
        self.world = world
        self.name = name
        self.entity = entity  # will be set when added to an entity
        self.active = True
        self.activation_type = activation_type # e.g., "ON_STEP", "ON_INTERACT"
        self.walkable = activation_type == "ON_STEP"  # if ON_STEP, the event tile is walkable
        self.action_type = action_type # e.g., "MOVE", "DIALOGUE"
        self.kwargs = kwargs
        self.necessary_args = []

        # vérification que les argumetns nécessaires sont présents selon le type d'action
        if self.action_type == "MOVE":
            self.necessary_args = ["target_scene", "target_position"]
        elif self.action_type == "DIALOGUE":
            self.necessary_args = ["dialogue"]
        self.check_event_args(self.necessary_args, kwargs)

    def check_event_args(self, required_args, kwargs):
        missing = [arg for arg in required_args if arg not in kwargs]
        if missing:
            logger.warning(f"Event {self.name} dans {self.world} désactivé : arguments manquants {missing}")
            self.active = False

    @property
    def position(self):
        return self.entity.position

    def is_facing_player(self):
        x, y = self.data.player.position
        dx, dy = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}.get(
            self.data.player.orientation, (0, 0)
        )
        return (x + dx, y + dy) == self.position


    # activation stuff
    def activation(self):
        if self.active:
            if self.action_type == "MOVE":
                self.data.set_scene(self.kwargs["target_scene"])
                self.data.player.position = self.kwargs["target_position"]
            elif self.action_type == "DIALOGUE":
                self.data.mode_change("dialogue")
                self.data.dialogue_system.set_dialogues(self.kwargs["dialogue"])

    def should_trigger(self, action):
        if self.activation_type == "ON_STEP":
            return self.data.player.position == self.position
        elif self.activation_type == "ON_INTERACT":
            return self.is_facing_player() and action == "INTERACT"
        return False



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
    def __init__(self, world, position):
        super().__init__(world, "Hero", position, '@')
        self.movable = True

        self.orientation = "DOWN"  # Possible orientations: UP, DOWN, LEFT, RIGHT

        self.inventory = { # dictionnary, id of the item is the key, the value is the quantity

        }
        if charged:
            self.ext_data = data_ext.player_data




    def facing_position(self): # gives the tiles facing the player
        x, y = self.position
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