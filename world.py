from engine.core.base import World, Entity, Event, NPC


class Village1(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Village1", "assets/maps/village1.txt")
        self.name = "Village1"

        #Exemple type de l'event door
        self.add_entity(Entity(self, "aPreciser", (11, 12), 'D',
                               [Event(data, self,"aPreciser", "ON_INTERACT", "MOVE",
                                      target_scene=Village2, target_position=(15, 5))]))

        #transition to guild
        self.add_entity(Entity(self, "guildEntry", (11, 12), 'D',
                               [Event(data, self, "guildEntry", "ON_INTERACT", "MOVE",
                                      target_scene=Guild, target_position=(13, 31))]))
        self.add_entity(Entity(self, "guildEntry", (11, 13), 'D',
                               [Event(data, self, "guildEntry", "ON_INTERACT", "MOVE",
                                      target_scene=Guild, target_position=(13, 32))]))
        
        #transition to forge
        self.add_entity(Entity(self, "guildEntry", (11, 12), 'D',
                               [Event(data, self, "guildEntry", "ON_INTERACT", "MOVE",
                                      target_scene=Village1, target_position=(19, 21))]))
        self.add_entity(Entity(self, "guildEntry", (11, 13), 'D',
                               [Event(data, self, "guildEntry", "ON_INTERACT", "MOVE",
                                      target_scene=Village1, target_position=(19, 22))]))


        #transition to Village2
        self.add_entity(Entity(self, "bridgeBot", (18, 36), ' ',
                               [Event(data, self,"bridgeBot", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 36))]))
        self.add_entity(Entity(self, "bridgeBot", (18, 37), ' ',
                               [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 37))]))
        self.add_entity(Entity(self, "bridgeBot", (18, 38), ' ',
                               [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(2, 38))]))

        #transition to forest
        self.add_entity(Entity(self, "forestTop", (1, 36), ' ',
                               [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                      target_scene=Forest, target_position=(17, 36))]))
        self.add_entity(Entity(self, "forestTop", (1, 37), ' ',
                               [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                      target_scene=Forest, target_position=(17, 37))]))
        self.add_entity(Entity(self, "forestTop", (1, 38), ' ',
                               [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                      target_scene=Forest, target_position=(17, 38))]))

        #exemple type de l'event NPC
        self.add_entity(NPC(self, "npc1", (4, 5), 'N', dialogue="assets/dialogues/Village.json"))


class Guild(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/guild.txt", (0, 0))
        self.name = "Guild"

        #exit guild
        self.add_entity(Entity(self, "guildExit", (19, 21), 'D',
                               [Event(data, self, "guildExit", "ON_INTERACT", "MOVE",
                                      target_scene=Village1, target_position=(11, 12))]))
        self.add_entity(Entity(self, "guildExit", (19, 22), 'D',
                               [Event(data, self, "guildExit", "ON_INTERACT", "MOVE",
                                      target_scene=Village1, target_position=(11, 13))]))

        #librarian
        self.add_entity(NPC(self, "librarian", (6, 11), 'L', dialogue="assets/dialogues/librarian.json"))


class Forge(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "assets/maps/forge.txt", (0, 0))
        self.name = "Forge"

        self.add_entity(Entity(self, "forgeExit", (13, 31), 'D',
                               [Event(data, self, "forgeExit", "ON_INTERACT", "MOVE",
                                      target_scene=Village1, target_position=(10, 55))]))
        self.add_entity(Entity(self, "forgeExit", (13, 32), 'D',
                               [Event(data, self, "forgeExit", "ON_INTERACT", "MOVE",
                                      target_scene=Village1, target_position=(10, 56))]))


class Village2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Village2", "assets/maps/village2.txt")
        self.name = "Village2"

        self.add_entity(Entity(self, "bridgeTop", (1, 36), ' ',
                               [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(17, 36))]))
        self.add_entity(Entity(self, "bridgeTop", (1, 37), ' ',
                               [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(17, 37))]))
        self.add_entity(Entity(self, "bridgeTop", (1, 38), ' ',
                               [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(17, 38))]))

        #transition to zoo
        self.add_entity(Entity(self, "zooLeft", (11, 1), ' ',
                               [Event(data, self, "zooLeft", "ON_STEP", "MOVE",
                                      target_scene=Zoo, target_position=(10, 68))]))


class Zoo(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Zoo", "assets/maps/zoo.txt")
        self.name = "Zoo"

        self.add_entity(Entity(self, "zooBot", (10, 69), ' ',
                               [Event(data, self, "zooBot", "ON_STEP", "MOVE",
                                      target_scene=Village2, target_position=(11, 2))]))


class Forest(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Forest", "assets/maps/forest.txt")
        self.name = "Forest"

        #transition to village1
        self.add_entity(Entity(self, "forestBot", (19, 31), ' ',
                               [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(2, 30))]))
        self.add_entity(Entity(self, "forestBot", (19, 32), ' ',
                               [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(2, 31))]))
        self.add_entity(Entity(self, "forestBot", (19, 33), ' ',
                               [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                      target_scene=Village1, target_position=(2, 32))]))

        #transition to cave
        self.add_entity(Entity(self, "caveEntry", (11, 30), 'C',
                               [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                      target_scene=Cave, target_position=(19, 31))]))
        self.add_entity(Entity(self, "caveEntry", (11, 31), 'C',
                               [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                      target_scene=Cave, target_position=(19, 32))]))
        self.add_entity(Entity(self, "caveEntry", (11, 32), 'C',
                               [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                      target_scene=Cave, target_position=(19, 33))]))


class Cave(World):
    def __init__(self, data, **kwargs):
        super().__init__(data, "Cave", "assets/maps/cave.txt")
        self.name = "Cave"

        #transition to forest
        self.add_entity(Entity(self, "caveExit", (19, 31), 'C',
                               [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                      target_scene=Forest, target_position=(11, 30))]))
        self.add_entity(Entity(self, "caveExit", (19, 32), 'C',
                               [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                      target_scene=Forest, target_position=(11, 31))]))
        self.add_entity(Entity(self, "caveExit", (19, 33), 'C',
                               [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                      target_scene=Forest, target_position=(11, 32))]))