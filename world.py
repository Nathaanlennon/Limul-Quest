from engine.core.base import World, Entity, Event, NPC


def Village1(data):
    self = World(data, "Village1", "assets/maps/village1.txt")

    # transition to guild
    self.add_entity(Entity(self, "guildEntryG", (10, 11), 'D',
                           [Event(data, self, "guildEntryG", "ON_INTERACT", "MOVE",
                                  target_scene="Guild", target_position=(11, 30))]))
    self.add_entity(Entity(self, "guildEntryD", (10, 12), 'D',
                           [Event(data, self, "guildEntryD", "ON_INTERACT", "MOVE",
                                  target_scene="Guild", target_position=(11, 31))]))

    # transition to forge
    self.add_entity(Entity(self, "forgeEntryG", (9, 54), 'D',
                           [Event(data, self, "forgeEntryG", "ON_INTERACT", "MOVE",
                                  target_scene="Forge", target_position=(17, 20))]))
    self.add_entity(Entity(self, "forgeEntryD", (9, 55), 'D',
                           [Event(data, self, "forgeEntryD", "ON_INTERACT", "MOVE",
                                  target_scene="Forge", target_position=(17, 21))]))

    # transition to Village2
    self.add_entity(Entity(self, "bridgeBot", (18, 36), ' ',
                           [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(2, 36))], True))
    self.add_entity(Entity(self, "bridgeBot", (18, 37), ' ',
                           [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(2, 37))], True))
    self.add_entity(Entity(self, "bridgeBot", (18, 38), ' ',
                           [Event(data, self, "bridgeBot", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(2, 38))], True))

    # transition to forest
    self.add_entity(Entity(self, "forestTop1", (1, 32), ' ',
                           [Event(data, self, "forestTop1", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(17, 32))], True))
    self.add_entity(Entity(self, "forestTop2", (1, 33), ' ',
                           [Event(data, self, "forestTop2", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(17, 33))], True))
    self.add_entity(Entity(self, "forestTop", (1, 34), ' ',
                           [Event(data, self, "forestTop", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(17, 34))], True))
    return self


def Guild(data):
    self = World(data, "Guild", "assets/maps/guild.txt")

    # exit guild
    self.add_entity(Entity(self, "guildExitG", (12, 30), 'D',
                           [Event(data, self, "guildExitG", "ON_INTERACT", "MOVE",
                                  target_scene="Village1", target_position=(11, 11))]))
    self.add_entity(Entity(self, "guildExitD", (12, 31), 'D',
                           [Event(data, self, "guildExitD", "ON_INTERACT", "MOVE",
                                  target_scene="Village1", target_position=(11, 12))]))

    # librarian
    self.add_entity(NPC(self, "librarian", (6, 11), 'L', dialogue="assets/dialogues/librarian.json"))

    # teacher
    self.add_entity(NPC(self, "teacher", (7, 37), 'E', dialogue="assets/dialogues/teacher.json"))

    # banker
    self.add_entity(NPC(self, "banker", (6, 59), 'B', dialogue="assets/dialogues/banker.json"))
    return self


def Forge(data):
    self = World(data, "Forge", "assets/maps/forge.txt")

    self.add_entity(Entity(self, "forgeExitG", (18, 20), 'D',
                           [Event(data, self, "forgeExitG", "ON_INTERACT", "MOVE",
                                  target_scene="Village1", target_position=(10, 54))]))
    self.add_entity(Entity(self, "forgeExitD", (18, 21), 'D',
                           [Event(data, self, "forgeExitD", "ON_INTERACT", "MOVE",
                                  target_scene="Village1", target_position=(10, 55))]))

    # blacksmith
    self.add_entity(NPC(self, "blacksmith", (12, 15), 'B', dialogue="assets/dialogues/blacksmith.json"))
    return self


def Village2(data):
    self = World(data, "Village2", "assets/maps/village2.txt")

    self.add_entity(Entity(self, "bridgeTop", (1, 36), ' ',
                           [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(17, 36))], True))
    self.add_entity(Entity(self, "bridgeTop", (1, 37), ' ',
                           [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(17, 37))], True))
    self.add_entity(Entity(self, "bridgeTop", (1, 38), ' ',
                           [Event(data, self, "bridgeTop", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(17, 38))], True))

    # transition to zoo
    self.add_entity(Entity(self, "zooLeft", (11, 1), ' ',
                           [Event(data, self, "zooLeft", "ON_STEP", "MOVE",
                                  target_scene="Zoo", target_position=(10, 68))], True))
    return self


def Zoo(data):
    self = World(data, "Zoo", "assets/maps/zoo.txt")

    self.add_entity(Entity(self, "zooRight", (10, 69), ' ',
                           [Event(data, self, "zooRight", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(11, 2))], True))
    return self


def Forest(data):
    self = World(data, "Forest", "assets/maps/forest.txt")

    # transition to village1
    self.add_entity(Entity(self, "forestBot", (18, 32), ' ',
                           [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(2, 31))], True))
    self.add_entity(Entity(self, "forestBot", (18, 33), ' ',
                           [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(2, 32))], True))
    self.add_entity(Entity(self, "forestBot", (18, 34), ' ',
                           [Event(data, self, "forestBot", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(2, 33))], True))

    # transition to cave
    self.add_entity(Entity(self, "caveEntry", (11, 32), ' ',
                           [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 31))], True))
    self.add_entity(Entity(self, "caveEntry", (11, 33), ' ',
                           [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 32))], True))
    self.add_entity(Entity(self, "caveEntry", (11, 34), ' ',
                           [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 33))], True))
    self.add_entity(Entity(self, "caveEntry", (11, 35), ' ',
                           [Event(data, self, "caveEntry", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 34))], True))
    return self


def Cave(data):
    self = World(data, "Cave", "assets/maps/cave.txt")

    # transition to forest
    self.add_entity(Entity(self, "caveExit", (18, 31), ' ',
                           [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 32))], True))
    self.add_entity(Entity(self, "caveExit", (18, 32), ' ',
                           [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 33))], True))
    self.add_entity(Entity(self, "caveExit", (18, 33), ' ',
                           [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 34))], True))
    self.add_entity(Entity(self, "caveExit", (18, 34), ' ',
                           [Event(data, self, "caveExit", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 35))], True))
    return self