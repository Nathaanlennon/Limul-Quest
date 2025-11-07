from engine.core.base import World, Entity, Event, NPC


class Test(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/village2.txt", (12, 30))
        self.name = "Monde1"

        #bucher's door

        self.add_entity(Entity(self, "door1", (9, 13), 'D',
                               [Event(data, self,"door1", "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(5, 5))]))
        self.add_entity(Entity(self, "door2", (9, 14), 'D',
                               [Event(data, self,"door2", "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(5, 5))]))
        
        #theatre door

        self.add_entity(Entity(self, "door3", (14, 52), 'D',
                               [Event(data, self,"door3", "ON_INTERACT", "MOVE",
                  target_scene=Test2, target_position=(5, 5))]))
        
        #transition to village1

        self.add_entity(Entity(self, "teleporter1", (1, 36), ' ',
                               [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3))]))
        
        self.add_entity(Entity(self, "teleporter1", (1, 37), ' ',
                               [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3))]))
        
        self.add_entity(Entity(self, "teleporter1", (1, 38), ' ',
                               [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3))]))
        
        # transition to zoo map

        self.add_entity(Entity(self, "teleporter1", (11, 1), ' ',
                               [Event(data, self,"teleporter1", "ON_STEP", "MOVE",
                  target_scene=Test, target_position=(3, 3))]))
        
        # npcs

        self.add_entity(NPC(self, "npc1", (10, 32), 'N', dialogue="assets/dialogues/test.json"))


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
