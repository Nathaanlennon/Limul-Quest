class EventSystem:
    def __init__(self, world):
        self.world = world
        self.events = {} # key is the (x,y) coordinates of the event



    def add_event(self, event):
        self.events[event.position] = event

    def remove_event(self, event):
        if event.position in self.events:
            del self.events[event.position]

    def get_event(self, position):
        return self.events.get(position, 0)

    def update(self, player, action):
        if action == "INTERACT":
            event = self.get_event(player.facing_position())
        else :
            event = self.get_event(player.position)

        if event and event.should_trigger(action):
            event.activation()