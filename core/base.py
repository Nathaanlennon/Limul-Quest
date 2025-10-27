from core.EventSystem import EventSystem


class UniversData:
    def __init__(self, scene):
        self.scenes = {}
        self.current_scene = None
        self.player = Player(self.current_scene, self.current_scene.spawn_player if self.current_scene else (2, 2))
        self.set_scene(scene)

        self.mode = "exploration"  # Possible modes: : exploration, combat, dialogue, inventory
        self.on_mode_change = None

    def set_mode_change_callback(self, callback):
        """L’UI nous donne la fonction à appeler plus tard"""
        self.on_mode_change = callback

    def mode_change(self, mode):
        self.mode = mode
        self.on_mode_change(mode)

    def add_scene(self, scene_class,
                  **kwargs):  # args et kwargs servent à dire qu'on peut mettre autant de paramètres qu'on veut, utile pour le chargement d'une sauvegarde
        if scene_class not in self.scenes:
            self.scenes[scene_class] = scene_class(self, **kwargs)

    def set_scene(self, scene_class, **kwargs):
        self.add_scene(scene_class, **kwargs)
        self.current_scene = self.scenes[scene_class]
        self.player.position = self.current_scene.spawn_player
        self.player.world = self.current_scene

    def get_scene(self):
        return self.current_scene

    def load_save(self):
        ...  # Implémentation du chargement de sauvegarde à venir


class World:
    def __init__(self, data, map, spawn_player, **kwargs):
        self.data = data
        self.walkable_tiles = ['.', ',', ';', ':', '+', '*', ' ']
        self.entities = []
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
        self.entities.append(entity)



class Entity:
    def __init__(self, world, name, position, sprite, **kwargs):
        self.name = name
        self.position = position
        self.sprite = sprite
        self.world = world
        self.movable = False

    def move(self, dx, dy):
        x, y = self.position
        if self.world.is_walkable((x+dx, y+dy)) and self.movable:
            self.position = (x + dx, y + dy)



class Event(Entity):
    def __init__(self, data, world, name, position, sprite, **kwargs):
        super().__init__(world, name, position, sprite)
        self.data = data
        self.active = True
        self.walkable = False

    def activation(self):
        pass

    def should_trigger(self, action):
        pass

    def is_facing_player(self):
        x, y = self.data.player.position
        dx, dy = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}.get(
            self.data.player.orientation, (0, 0)
        )
        return (x + dx, y + dy) == self.position


class MoveEvent(Event):
    def __init__(self, data, world, name, position, target_scene, target_position, move_type):
        super().__init__(data, world, name, position, '0')
        if move_type == "teleport":
            self.sprite = 'T'
            self.walkable = True
        elif move_type == "door":
            self.sprite = 'D'


        self.target_scene = target_scene
        self.target_position = target_position
        self.type = move_type

    def activation(self):
        if self.active:
            self.data.set_scene(self.target_scene)
            self.data.player.position = self.target_position

    def should_trigger(self, action):
        if self.type == "teleport":
            return self.data.player.position == self.position
        if self.type == "door":
            return self.is_facing_player() and action == "INTERACT"
        return False

class NPC(Entity):
    def __init__(self, world, name, position, sprite, **kwargs):
        super().__init__(world, name, position, sprite)


class Player(Entity):
    def __init__(self, world, position):
        super().__init__(world, "Hero", position, '@')
        self.movable = True

        self.orientation = "DOWN"  # Possible orientations: UP, DOWN, LEFT, RIGHT

    def facing_position(self): # gives the tiles facing the player
        x, y = self.position
        dx, dy = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}.get(
            self.orientation, (0, 0)
        )
        return x + dx, y + dy