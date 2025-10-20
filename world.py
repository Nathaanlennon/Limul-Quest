from core.base import MoveEvent
from core.base import World


class Test(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"assets/maps/maptest.txt", (2, 3))
        self.name = "Monde1"
        self.map_data = self.load_map()

        self.event_system.add_event(MoveEvent(data, self,"door", (4,11), Test2, (5,5),"door"))
        self.event_system.add_event(MoveEvent(data, self,"teleporter", (5,1), Test, (3,3),"teleport"))


class Test2(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"assets/maps/testchateau.txt", (5, 5))
        self.name = "Monde2"
        self.map_data = self.load_map()


class Test3(World):
    def __init__(self, data, **kwargs):
        super().__init__(data,"assets/maps/test_village.txt", (3, 3))
        self.name = "Monde3"
        self.map_data = self.load_map()