from engine.core.base import World, Entity, Event, NPC


class Test(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Monde1", "assets/maps/village2.txt")

        self.add_entity(Entity(self, "door1", (4, 11), 'DD',
                               [Event(data, self,"door1", "ON_INTERACT", "MOVE",
                  target_scene="Monde2", target_position=(5, 5))]))
        self.add_entity(Entity(self, "teleporter1", (5, 1), 'T',
                             [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene="Monde1", target_position=(3, 3))], True))

        self.add_entity(NPC(self, "npc1", (3, 1), 'N', dialogue="assets/dialogues/test.json"))
        self.event_system.add_event(Event(data, self, "combat_event", "ALWAYS","COMBAT",
                                          enemies=[
                                              ("goblin",1),
                                              ("goblin",1)
                                          ], proba=0))
        self.add_entity(Entity(self, "test", (3,2), 'I',[
            Event(data, self, "test", "ON_INTERACT","MODE_CHANGE", mode="saucisse")]))




class Test2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Monde2", "assets/maps/testchateau.txt")

        entity = self.add_entity(Entity(self,"door", (8, 24), 'D'))
        entity.add_event(Event(data, self, "door","ON_INTERACT", "MOVE",
                               target_scene="Monde3", target_position=(3, 3)))


class Test3(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Monde3", "assets/maps/test_village.txt")

        entity = self.add_entity(Entity(self,"door", (9, 24), 'D'))
        entity.add_event(Event(data, self, "door","ON_INTERACT", "MOVE",
                  target_scene="Monde2", target_position=(1, 1)))

