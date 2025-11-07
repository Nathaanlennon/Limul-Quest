from engine.core.base import World, Entity, Event, NPC


class Test(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/maptest.txt", (3, 3))
        self.name = "Monde1"

        self.add_entity(Entity(self, "door1", (5, 5), 'D',
                               [Event(data, self,"door1", "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(15, 5))]))
        self.add_entity(Entity(self, "teleporter1", (3, 1), 'T',
                               [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3))]))

        self.add_entity(NPC(self, "npc1", (1, 1), 'N', dialogue="assets/dialogues/test.json"))


class Test2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/mapVillageV1.txt", (5, 5))
        self.name = "Monde2"

        self.add_entity(Entity(self,"door2", (8, 24), 'D',
                               [Event(data, self,"door2", "ON_INTERACT", "MOVE",
                                      target_scene=Test, target_position=(9, 35))]))
        self.add_entity(Entity(self, "teleporter2", (11, 35), 'T',
                               [Event(data, self, "teleporter2", "ON_STEP", "MOVE",
                                      target_scene=Test2, target_position=(5, 5))]))


class Test3(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/test_village.txt", (3, 3))
        self.name = "Monde3"

        entity = self.add_entity(Entity(self,"door", (9, 24), 'D'))
        entity.add_event(Event(data, self, "door","ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(1, 1)))
