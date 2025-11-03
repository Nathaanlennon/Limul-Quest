import curses
import world

# mapping global, créé une seule fois
KEY_MAPPING = {
    ord('z'): "UP", ord('Z'): "UP",
    ord('s'): "DOWN", ord('S'): "DOWN",
    ord('q'): "LEFT", ord('Q'): "LEFT",
    ord('d'): "RIGHT", ord('D'): "RIGHT",
    ord('e'): "INTERACT", ord('E'): "INTERACT",
    ord('x'): "QUIT", ord('X'): "QUIT",
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
}

# chiffres 0-9 → renvoie directement l'entier
for i in range(10):
    KEY_MAPPING[ord(str(i))] = i

def key_to_action(key):
    return KEY_MAPPING.get(key, None)




class CursesUI:
    def __init__(self, universe):
        self.universe = universe
        self.modes = {
            "exploration": self.exploration_mode,
            "dialogue": self.dialogue_mode
        }
        self.mode_draw_function = self.modes[universe.mode]
        self.universe.set_mode_change_callback(self.change_mode)


    def run(self):
        curses.wrapper(self.main_loop)

    def change_mode(self, mode):
        self.mode_draw_function = self.modes[mode]

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False) # getch make things waiting | edit I have no idea wtf this means

        while True:
            stdscr.erase()
            if stdscr.getmaxyx()[0] <= self.universe.size[0] or stdscr.getmaxyx()[1] <= self.universe.size[1]:
                stdscr.addstr(0, 0, "Veuillez agrandir la fenêtre")

            else:
                self.mode_draw_function(stdscr)
                key = stdscr.getch()
                self.universe.input_system(self.universe, key_to_action(key))# traite l'entrée et la convertit en action que le système peut comprendre

                if key == ord('r'):
                    self.universe.set_scene(world.Test)
                elif key == ord('n'):
                    self.universe.set_scene(world.Test2)
                elif key == ord('y'):
                    self.universe.set_scene(world.Test3)
                elif key == ord('m'):
                    self.universe.mode_change("dialogue")
                elif key == ord('p'):
                    self.universe.mode_change("exploration")

            stdscr.refresh()


    def exploration_mode(self, stdscr):
        self.show_scene(stdscr)
        self.draw_player(stdscr)
        self.draw_entities(stdscr)
        # self.draw_events(stdscr) # events dont have sprite for now



    def dialogue_mode(self, stdscr):
        stdscr.addstr(0, 0, self.universe.dialogue_system.current_reading)
        if self.universe.dialogue_system.state == "CHOICE":
            for idx, choice in enumerate(self.universe.dialogue_system.choices):
                stdscr.addstr(idx + 2, 0, f"{idx + 1}. {choice}")


    def show_scene(self, stdscr):
        scene = self.universe.current_scene
        for y, ligne in enumerate(scene.map_data):
            stdscr.addstr(y, 0, ligne)
        stdscr.addstr(len(scene.map_data)+1, 0, "Appuie sur 'q' pour quitter.")

    def draw_player(self, stdscr):
        player = self.universe.player
        y, x = player.position
        stdscr.addstr(y, x, player.sprite)

    def draw_entity(self, stdscr, entity):
        y, x = entity.position
        stdscr.addstr(y, x, entity.sprite)
    def draw_entities(self, stdscr):
        scene = self.universe.current_scene
        for entity in scene.entities.values():
            self.draw_entity(stdscr, entity)

    def draw_event(self, stdscr, event):
        y, x = event.position
        stdscr.addstr(y, x, event.sprite)
    def draw_events(self, stdscr):
        scene = self.universe.current_scene
        for event in scene.event_system.events.values():
            self.draw_event(stdscr, event)