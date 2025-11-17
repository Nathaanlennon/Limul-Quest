from engine.core.base import World, Entity, Event, NPC


class Village1(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/village1.txt", (3, 3))
        self.name = "Village1"

        self.add_entity(Entity(self, "aPreciser", (5, 5), 'D',
                               [Event(data, self,"aPreciser", "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(15, 5))]))
        self.add_entity(Entity(self, "pontBas", (19, 37), 'T',
                               [Event(data, self,"pontBas", "ON_STEP", "MOVE",
                  target_scene=Village2, target_position=(2, 37))]))
        self.add_entity(Entity(self, "pontBas", (19, 38), 'T',
                               [Event(data, self, "pontBas", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 38))]))
        self.add_entity(Entity(self, "pontBas", (19, 39), 'T',
                               [Event(data, self, "pontBas", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 39))]))
        self.add_entity(NPC(self, "npc1", (1, 1), 'N', dialogue="assets/dialogues/test.json"))


class Village2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/village2.txt", (5, 5))
        self.name = "Village2"

        self.add_entity(Entity(self,"aPreciser", (8, 24), 'D',
                               [Event(data, self,"aPreciser", "ON_INTERACT", "MOVE",
                                      target_scene=Test, target_position=(9, 35))]))
        self.add_entity(Entity(self, "pontHaut", (2, 37), 'T',
                               [Event(data, self, "pontHaut", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(19, 37))]))
        self.add_entity(Entity(self, "pontHaut", (2, 38), 'T',
                               [Event(data, self, "pontHaut", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(19, 38))]))
        self.add_entity(Entity(self, "pontHaut", (2, 39), 'T',
                               [Event(data, self, "pontHaut", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(19, 39))]))


class Zoo(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/zoo.txt", (3, 3))
        self.name = "Zoo"

        entity = self.add_entity(Entity(self,"door", (9, 24), 'D'))
        entity.add_event(Event(data, self, "door","ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(1, 1)))
