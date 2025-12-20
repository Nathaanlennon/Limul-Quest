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
    self.add_entity(Entity(self, "bridgeBot1", (18, 36), ' ',
                           [Event(data, self, "bridgeBot1", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(2, 36))], True))
    self.add_entity(Entity(self, "bridgeBot2", (18, 37), ' ',
                           [Event(data, self, "bridgeBot2", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(2, 37))], True))
    self.add_entity(Entity(self, "bridgeBot3", (18, 38), ' ',
                           [Event(data, self, "bridgeBot3", "ON_STEP", "MOVE",
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
    self.add_entity(Entity(self, "librarian", (6, 11), 'L',
                        [Event(data, self, "librarian", "ON_INTERACT", "MODE_CHANGE", mode = "library")]))

    # teacher
    self.add_entity(NPC(self, "teacher", (7, 37), 'E', dialogue="assets/dialogues/teacher.json"))

    # banker
    self.add_entity(Entity(self, "banker", (6, 59), 'B',
                        [Event(data, self, "banker", "ON_INTERACT", "MODE_CHANGE", mode = "bank")]))
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
    self.add_entity(NPC(self, "blacksmith", (12, 15), 'F', dialogue="assets/dialogues/blacksmith.json"))
    return self


def Village2(data, **kwargs):
    self = World(data, "Village2", "assets/maps/village2.txt")

    self.add_entity(Entity(self, "bridgeTop1", (1, 36), ' ',
                           [Event(data, self, "bridgeTop1", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(17, 36))], walkable=True))
    self.add_entity(Entity(self, "bridgeTop2", (1, 37), ' ',
                           [Event(data, self, "bridgeTop2", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(17, 37))], walkable=True))
    self.add_entity(Entity(self, "bridgeTop3", (1, 38), ' ',
                           [Event(data, self, "bridgeTop3", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(17, 38))], walkable=True))

    # door for the butcher house
    self.add_entity(Entity(self, "door1Butcher", (9, 13), 'D',
                           [Event(data, self, "door1Butcher", "ON_INTERACT", "MOVE",
                                  target_scene="ButcherHouse", target_position=(15, 34))]))
    self.add_entity(Entity(self, "door2Butcher", (9, 14), 'D',
                           [Event(data, self, "door2Butcher", "ON_INTERACT", "MOVE",
                                  target_scene="ButcherHouse", target_position=(15, 35))]))

    # door for the theatre
    self.add_entity(Entity(self, "doorTheatre", (16, 54), 'D',
                           [Event(data, self, "doorTheatre", "ON_INTERACT", "MOVE",
                                  target_scene="Theatre", target_position=(14, 47))]))

    # transition to zoo
    self.add_entity(Entity(self, "zooLeft", (11, 1), ' ',
                           [Event(data, self, "zooLeft", "ON_STEP", "MOVE",
                                  target_scene="Zoo", target_position=(10, 68))], walkable=True))

    self.add_entity(NPC(self, "npc1", (11, 52), 'N', dialogue="assets/dialogues/test.json"))

    return self


def ButcherHouse(data, **kwargs):
    self = World(data, "ButcherHouse", "assets/maps/butcherHouse.txt")

    self.add_entity(Entity(self, "door1Butcher", (16, 34), 'D',
                           [Event(data, self, "door1Butcher", "ON_INTERACT", "MOVE",
                                  target_scene="Village2", target_position=(10, 13))]))
    self.add_entity(Entity(self, "door2Butcher", (16, 35), 'D',
                           [Event(data, self, "door2Butcher", "ON_INTERACT", "MOVE",
                                  target_scene="Village2", target_position=(10, 14))]))
    return self


def Theatre(data, **kwargs):
    self = World(data, "Theatre", "assets/maps/theatre.txt")

    self.add_entity(Entity(self, "doorToVillage2", (14, 48), 'D',
                           [Event(data, self, "doorToVillage2", "ON_INTERACT", "MOVE",
                                  target_scene="Village2", target_position=(16, 55))]))

    self.add_entity(NPC(self, "npc1", (10, 34), 'N', dialogue="assets/dialogues/test.json"))

    return self


def zooKeeperHouse(data, **kwargs):
    self = World(data, "zooKeeperHouse", "assets/maps/zooKeeperHouse.txt")

    self.add_entity(Entity(self, "door1Keeper", (14, 34), 'D',
                           [Event(data, self, "door1Keeper", "ON_INTERACT", "MOVE",
                                  target_scene="Zoo", target_position=(18, 55))]))
    self.add_entity(Entity(self, "door2Keeper", (14, 35), 'D',
                           [Event(data, self, "door2Keeper", "ON_INTERACT", "MOVE",
                                  target_scene="Zoo", target_position=(18, 56))]))

    self.add_entity(NPC(self, "zooKeeper", (8, 44), 'N', dialogue="assets/dialogues/test.json"))

    return self


def Zoo(data, **kwargs):
    self = World(data, "Zoo", "assets/maps/zoo.txt")

    self.add_entity(Entity(self, "zooBot", (10, 69), ' ',
                           [Event(data, self, "zooBot", "ON_STEP", "MOVE",
                                  target_scene="Village2", target_position=(11, 2))], walkable=True))
    self.add_entity(Entity(self, "door1Keeper", (17, 55), 'D',
                           [Event(data, self, "door1Keeper", "ON_INTERACT", "MOVE",
                                  target_scene="zooKeeperHouse", target_position=(13, 34))]))
    self.add_entity(Entity(self, "door2Keeper", (17, 56), 'D',
                           [Event(data, self, "door2Keeper", "ON_INTERACT", "MOVE",
                                  target_scene="zooKeeperHouse", target_position=(13, 35))]))

    # we are going to use the already existing class npc for the signs in the zoo
    self.add_entity(
        NPC(self, "sign1", (6, 13), '🪧', dialogue="assets/dialogues/testZoo.json"))  # chat gpt dialogue for now
    self.add_entity(NPC(self, "sign1", (6, 14), '',
                        dialogue="assets/dialogues/test.json"))  # need this one cause sign is two caracter

    self.add_entity(NPC(self, "sign2", (6, 30), '🪧', dialogue="assets/dialogues/test.json"))
    self.add_entity(NPC(self, "sign2.1", (6, 31), '', dialogue="assets/dialogues/test.json"))

    self.add_entity(NPC(self, "sign3", (6, 46), '🪧', dialogue="assets/dialogues/test.json"))
    self.add_entity(NPC(self, "sign3.1", (6, 47), '', dialogue="assets/dialogues/test.json"))

    self.add_entity(NPC(self, "sign4", (6, 63), '🪧', dialogue="assets/dialogues/test.json"))
    self.add_entity(NPC(self, "sign4.1", (6, 62), '', dialogue="assets/dialogues/test.json"))

    self.add_entity(NPC(self, "sign5", (13, 13), '🪧', dialogue="assets/dialogues/test.json"))
    self.add_entity(NPC(self, "sign5.1", (13, 14), '', dialogue="assets/dialogues/test.json"))

    self.add_entity(NPC(self, "sign6", (13, 30), '🪧', dialogue="assets/dialogues/test.json"))
    self.add_entity(NPC(self, "sign6.1", (13, 31), '', dialogue="assets/dialogues/test.json"))

    self.add_entity(NPC(self, "sign7", (13, 46), '🪧', dialogue="assets/dialogues/test.json"))
    self.add_entity(NPC(self, "sign7.1", (13, 47), '', dialogue="assets/dialogues/test.json"))

    return self


def Forest(data):
    self = World(data, "Forest", "assets/maps/forest.txt")

    # transition to village1
    self.add_entity(Entity(self, "forestBot1", (18, 32), ' ',
                           [Event(data, self, "forestBot1", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(2, 32))], True))
    self.add_entity(Entity(self, "forestBot2", (18, 33), ' ',
                           [Event(data, self, "forestBot2", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(2, 33))], True))
    self.add_entity(Entity(self, "forestBot3", (18, 34), ' ',
                           [Event(data, self, "forestBot3", "ON_STEP", "MOVE",
                                  target_scene="Village1", target_position=(2, 34))], True))

    # transition to cave
    self.add_entity(Entity(self, "caveEntry1", (10, 32), '',
                           [Event(data, self, "caveEntry1", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 31))], True))
    self.add_entity(Entity(self, "caveEntry2", (10, 33), '',
                           [Event(data, self, "caveEntry2", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 32))], True))
    self.add_entity(Entity(self, "caveEntry3", (10, 34), '',
                           [Event(data, self, "caveEntry3", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 33))], True))
    self.add_entity(Entity(self, "caveEntry4", (10, 35), '',
                           [Event(data, self, "caveEntry4", "ON_STEP", "MOVE",
                                  target_scene="Cave", target_position=(17, 34))], True))
    return self


def Cave(data):
    self = World(data, "Cave", "assets/maps/cave.txt")

    # transition to forest
    self.add_entity(Entity(self, "caveExit1", (18, 31), ' ',
                           [Event(data, self, "caveExit1", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 32))], True))
    self.add_entity(Entity(self, "caveExit2", (18, 32), ' ',
                           [Event(data, self, "caveExit2", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 33))], True))
    self.add_entity(Entity(self, "caveExit3", (18, 33), ' ',
                           [Event(data, self, "caveExit3", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 34))], True))
    self.add_entity(Entity(self, "caveExit4", (18, 34), ' ',
                           [Event(data, self, "caveExit4", "ON_STEP", "MOVE",
                                  target_scene="Forest", target_position=(12, 35))], True))

    self.event_system.add_event(Event(data, self, "combat_event", "ALWAYS", "COMBAT",
                                      enemies=[
                                          ("goblin", 0),
                                          ("goblin", 0.01),
                                          ("slime", 0.2),
                                          ("bat", 1)

                                      ], proba=0.15))

    return self

