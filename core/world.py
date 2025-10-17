class UniversData:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.player = Player()
        self.set_scene(Test2)

    def add_scene(self, scene_class,
                  **kwargs):  # args et kwargs servent à dire qu'on peut mettre autant de paramètres qu'on veut, utile pour le chargement d'une sauvegarde
        if scene_class not in self.scenes:
            self.scenes[scene_class] = scene_class(**kwargs)

    def set_scene(self, scene_class, **kwargs):
        self.add_scene(scene_class, **kwargs)
        self.current_scene = self.scenes[scene_class]

    def get_scene(self):
        return self.current_scene

    def load_save(self):
        ...  # Implémentation du chargement de sauvegarde à venir

class World:
    def __init__(self, **kwargs):
        self.walkable_tiles = ['.', ',', ';', ':', '+', '*', ' ']
        self.map = "../maps/void.txt" # empty map for initialisation

    def load_map(self):
        with open(self.map, 'r') as file:
            map_data = [line.rstrip('\n') for line in file]
        return map_data

    def is_walkable(self, tile):
        return tile in self.walkable_tiles

class Test(World):
    def __init__(self, **kwargs):
        super().__init__()
        self.map = "assets/maps/maptest.txt"
        self.name = "Monde1"
        self.map_data = self.load_map()

class Test2(World):
    def __init__(self, **kwargs):
        super().__init__()
        self.map = "assets/maps/testchateau.txt"
        self.name = "Monde2"
        self.map_data = self.load_map()

class Test3(World):
    def __init__(self, **kwargs):
        super().__init__()
        self.map = "assets/maps/test_village.txt"
        self.name = "Monde3"
        self.map_data = self.load_map()

class Player:
    def __init__(self, name="Hero", position=(2, 3)):
        self.name = name
        self.position = position
        self.sprite = '@'  # Symbole représentant le joueur sur la carte