class UniversData:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.player = Player(self.current_scene)
        self.set_scene(Test2)

        self.mode = "exploration"  # Possible modes: : exploration, combat, dialogue, inventory

    def add_scene(self, scene_class,
                  **kwargs):  # args et kwargs servent à dire qu'on peut mettre autant de paramètres qu'on veut, utile pour le chargement d'une sauvegarde
        if scene_class not in self.scenes:
            self.scenes[scene_class] = scene_class(**kwargs)

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
    def __init__(self, map,spawn_player, **kwargs):
        self.walkable_tiles = ['.', ',', ';', ':', '+', '*', ' ']
        self.entities = []
        self.map = map # empty map for initialisation
        self.spawn_player = spawn_player # Default spawn position for player

    def load_map(self):
        with open(self.map, 'r') as file:
            map_data = [line.rstrip('\n') for line in file]
        return map_data

    def is_walkable(self, tile):
        return tile in self.walkable_tiles

    def add_entity(self, entity):
        self.entities.append(entity)


class Test(World):
    def __init__(self, **kwargs):
        super().__init__("assets/maps/maptest.txt", (2,3))
        self.name = "Monde1"
        self.map_data = self.load_map()



class Test2(World):
    def __init__(self, **kwargs):
        super().__init__("assets/maps/testchateau.txt", (5,5))
        self.name = "Monde2"
        self.map_data = self.load_map()

class Test3(World):
    def __init__(self, **kwargs):
        super().__init__("assets/maps/test_village.txt", (3,3))
        self.name = "Monde3"
        self.map_data = self.load_map()

class Entity:
    def __init__(self, world,  name, position, sprite, **kwargs):
        self.name = name
        self.position = position
        self.sprite = sprite
        self.world = world

    def move(self, dx, dy):
        x, y = self.position
        if self.is_move_possible(dx, dy):
            self.position = (x + dx, y + dy)

    def is_move_possible(self, dx, dy):
        x, y = self.position
        return self.world.map_data[x + dx][y + dy] in self.world.walkable_tiles


class Player(Entity):
    def __init__(self, world):
        super().__init__(world, "Hero", (2, 3), '@')