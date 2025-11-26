from engine.core.base import World, Entity, Event, NPC


class Test(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/village2.txt", (2, 3))
        self.name = "Monde1"

        self.add_entity(Entity(self, "door1", (4, 11), 'DD',
                               [Event(data, self,"door1", "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(5, 5))]))
        self.add_entity(Entity(self, "teleporter1", (5, 1), 'T',
                               [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3))]))

        self.add_entity(NPC(self, "npc1", (3, 1), 'N', dialogue="assets/dialogues/test.json"))
        self.event_system.add_event(Event(data, self, "combat_event", "ALWAYS","COMBAT",
                                          enemies=[
                                              ("goblin",1),
                                              ("goblin",1)
                                          ], proba=0))




class Test2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/testchateau.txt", (5, 5))
        self.name = "Monde2"

        entity = self.add_entity(Entity(self,"door", (8, 24), 'D'))
        entity.add_event(Event(data, self, "door","ON_INTERACT", "MOVE",
                               target_scene=Test3))


class Test3(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/test_village.txt", (3, 3))
        self.name = "Monde3"

        entity = self.add_entity(Entity(self,"door", (9, 24), 'D'))
        entity.add_event(Event(data, self, "door","ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(1, 1)))

