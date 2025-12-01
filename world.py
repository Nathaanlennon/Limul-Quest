from engine.core.base import World, Entity, Event, NPC


class Village1(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"Village1", "assets/maps/village1.txt")

        #Exemple type de l'event door
        self.add_entity(Entity(self, "aPreciser", (5, 5), 'D',
                               [Event(data, self,"aPreciser", "ON_INTERACT", "MOVE",
                  target_scene="Village2", target_position=(15, 5))]))

        #transition to Village2
        self.add_entity(Entity(self, "bridgeBot", (18, 36), ' ',
                               [Event(data, self,"bridgeBot", "ON_STEP", "MOVE",
                  target_scene="Village2", target_position=(2, 36))]))
        self.add_entity(Entity(self, "bridgeBot", (18, 37), ' ',
                               [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                      target_scene="Village2", target_position=(2, 37))]))
        self.add_entity(Entity(self, "bridgeBot", (18, 38), ' ',
                               [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                      target_scene="Village2", target_position=(2, 38))]))

        #transition to forest
        self.add_entity(Entity(self, "forestTop", (1, 36), ' ',
                               [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                      target_scene="Forest", target_position=(17, 36))]))
        self.add_entity(Entity(self, "forestTop", (1, 37), ' ',
                               [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                      target_scene="Forest", target_position=(17, 37))]))
        self.add_entity(Entity(self, "forestTop", (1, 38), ' ',
                               [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                      target_scene="Forest", target_position=(17, 38))]))

        #exemple type de l'event NPC
        self.add_entity(NPC(self, "npc1", (4, 5), 'N', dialogue="assets/dialogues/Village.json"))



class ButcherHouse(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"ButcherHouse", "assets/maps/butcherHouse.txt")

        self.add_entity(Entity(self, "door1Butcher", (16, 34), 'D',
                               [Event(data, self, "door1Butcher", "ON_INTERACT", "MOVE",
                                      target_scene="Village2", target_position=(10, 13))]))
        self.add_entity(Entity(self, "door2Butcher", (16, 35), 'D',
                               [Event(data, self, "door2Butcher", "ON_INTERACT", "MOVE",
                                      target_scene="Village2", target_position=(10, 14))]))

class Village2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"Village2", "assets/maps/village2.txt")


        self.add_entity(Entity(self, "bridgeTop", (1, 36), ' ',
                               [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                      target_scene="Village1", target_position=(17, 36))]))
        self.add_entity(Entity(self, "bridgeTop", (1, 37), ' ',
                               [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                      target_scene="Village1", target_position=(17, 37))]))
        self.add_entity(Entity(self, "bridgeTop", (1, 38), ' ',
                               [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                      target_scene="Village1", target_position=(17, 38))]))
        
        self.add_entity(Entity(self, "door1Butcher", (9, 13), 'D',
                               [Event(data, self, "door1Butcher", "ON_INTERACT", "MOVE",
                                      target_scene="ButcherHouse", target_position=(15, 34))]))
        self.add_entity(Entity(self, "door2Butcher", (9, 14), 'D',
                               [Event(data, self, "door2Butcher", "ON_INTERACT", "MOVE",
                                      target_scene="ButcherHouse", target_position=(15, 35))]))

        #transition to zoo
        self.add_entity(Entity(self, "zooLeft", (11, 1), ' ',
                               [Event(data, self, "zooLeft", "ON_STEP", "MOVE",
                                      target_scene="Zoo", target_position=(10, 68))],walkable=True))

class zooKeeperHouse(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"zooKeeperHouse", "assets/maps/zooKeeperHouse.txt")


        self.add_entity(Entity(self, "door1Keeper", (16, 34), 'D',
                               [Event(data, self, "door1Keeper", "ON_INTERACT", "MOVE",
                                      target_scene="Zoo", target_position=(18, 55))]))
        self.add_entity(Entity(self, "door2Keeper", (16, 35), 'D',
                               [Event(data, self, "door2Keeper", "ON_INTERACT", "MOVE",
                                      target_scene="Zoo", target_position=(18, 56))]))
        
        self.add_entity(NPC(self, "zooKeeper", (11, 30), 'N', dialogue="assets/dialogues/test.json"))

        

class Zoo(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"Zoo", "assets/maps/zoo.txt")

        self.add_entity(Entity(self, "zooBot", (10, 69), ' ',
                               [Event(data, self, "zooBot", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(11, 2))]))
        self.add_entity(Entity(self, "door1Keeper", (17, 55), 'D',
                               [Event(data, self, "door1Keeper", "ON_INTERACT", "MOVE",
                                      target_scene="zooKeeperHouse", target_position=(15, 34))]))
        self.add_entity(Entity(self, "door2Keeper", (17, 56), 'D',
                               [Event(data, self, "door2Keeper", "ON_INTERACT", "MOVE",
                                      target_scene="zooKeeperHouse", target_position=(15, 35))]))
        


class Forest(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"Forest", "assets/maps/forest.txt")

        #transition to village1
        self.add_entity(Entity(self, "forestBot", (18, 36), ' ',
                               [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                      target_scene="Village1", target_position=(2, 36))]))
        self.add_entity(Entity(self, "forestBot", (18, 37), ' ',
                               [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                      target_scene="Village1", target_position=(2, 37))]))
        self.add_entity(Entity(self, "forestBot", (18, 38), ' ',
                               [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                      target_scene="Village1", target_position=(2, 38))]))

        #transition to cave
        self.add_entity(Entity(self, "forest", (6, 22), 'C',
                               [Event(data, self, "forest", "ON_STEP", "MOVE",
                                      target_scene="Cave", target_position=(17, 37))]))


class Cave(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"Cave", "assets/maps/cave.txt")

        #transition to forest
        self.add_entity(Entity(self, "entryCave", (18, 37), 'F',
                               [Event(data, self, "entryCave", "ON_STEP", "MOVE",
                                      target_scene="Forest", target_position=(7, 22))]))