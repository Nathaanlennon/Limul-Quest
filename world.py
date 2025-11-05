from core.base import *


class Test(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/taille.txt", (2, 3))
        self.name = "Monde1"

        entity = self.add_entity(Entity(self, "door1", (4, 11), '()'))
        entity.add_event(Event(data, "door1", entity, "ON_INTERACT", "MOVE",
                  target_scene=Test3, target_position=(5, 5)))
        entity = self.add_entity(Entity(self, "teleporter1", (5, 1), 'T'))
        entity.add_event(Event(data, "teleporter1", entity, "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3)))

        entity = self.add_entity(NPC(self, "npc1", (1, 1), 'N', dialogue="assets/dialogues/test.json"))


class Test2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/testchateau.txt", (5, 5))
        self.name = "Monde2"

        entity = self.add_entity(Entity(self,"door", (8, 24), 'D'))
        entity.add_event(Event(data, "door", entity, "ON_INTERACT", "MOVE",
                  target_scene=Test3,target_position=(5, 5)))


class Test3(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/test_village.txt", (3, 3))
        self.name = "Monde3"

        entity = self.add_entity(Entity(self,"door", (9, 24), 'D'))
        entity.add_event(Event(data, "door", entity, "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(1, 1)))
