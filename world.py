from engine.core.base import World, Entity, Event, NPC


class Village1(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/village1.txt", (10, 36))
        self.name = "Village1"

        #Exemple type de l'event door
        self.add_entity(Entity(self, "aPreciser", (5, 5), 'D',
                               [Event(data, self,"aPreciser", "ON_INTERACT", "MOVE",
                  target_scene=Village2, target_position=(15, 5))]))


        self.add_entity(Entity(self, "pontBas", (18, 36), ' ',
                               [Event(data, self,"pontBas", "ON_STEP", "MOVE",
                  target_scene=Village2, target_position=(2, 36))]))
        self.add_entity(Entity(self, "pontBas", (18, 37), ' ',
                               [Event(data, self, "pontBas", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 37))]))
        self.add_entity(Entity(self, "pontBas", (18, 38), ' ',
                               [Event(data, self, "pontBas", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 38))]))

        #exemple type de l'event NPC
        self.add_entity(NPC(self, "npc1", (4, 5), 'N', dialogue="assets/dialogues/Village.json"))


class Village2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/village2.txt", (5, 5))
        self.name = "Village2"

        self.add_entity(Entity(self, "pontHaut", (1, 36), ' ',
                               [Event(data, self, "pontHaut", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(17, 36))]))
        self.add_entity(Entity(self, "pontHaut", (1, 37), ' ',
                               [Event(data, self, "pontHaut", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(17, 37))]))
        self.add_entity(Entity(self, "pontHaut", (1, 38), ' ',
                               [Event(data, self, "pontHaut", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(17, 38))]))

        #transition to zoo
        self.add_entity(Entity(self, "zooGauche", (11, 1), ' ',
                               [Event(data, self, "zooGauche", "ON_STEP", "MOVE",
                                      target_scene=Zoo, target_position=(10, 68))]))

class Zoo(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/zoo.txt", (3, 3))
        self.name = "Zoo"

        self.add_entity(Entity(self, "zooDroite", (10, 69), ' ',
                               [Event(data, self, "zooDroite", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(11, 2))]))
