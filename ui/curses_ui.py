import curses
import world

def key_to_action(key):
    mapping = {
        ord('z'): "UP",
        ord('s'): "DOWN",
        ord('q'): "LEFT",
        ord('d'): "RIGHT",
        ord('e'): "INTERACT",
        curses.KEY_UP: "UP",
        curses.KEY_DOWN: "DOWN",
        curses.KEY_LEFT: "LEFT",
        curses.KEY_RIGHT: "RIGHT",
        ord('x'): "QUIT"
    }
    return mapping.get(key, None)


class CursesUI:
    def __init__(self, univers, input_system):
        self.univers = univers
        self.input_system = input_system
        self.modes = {
            "exploration": self.exploration_mode,
            "dialogue": self.dialogue_mode
        }
        self.mode_draw_function = self.modes[univers.mode]
        self.univers.set_mode_change_callback(self.change_mode)

    def run(self):
        curses.wrapper(self.main_loop)

    def change_mode(self, mode):
        self.mode_draw_function = self.modes[mode]

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)

        while True:
            stdscr.clear()
            self.mode_draw_function(stdscr)
            stdscr.refresh()


    def exploration_mode(self, stdscr):
        self.show_scene(stdscr)
        self.draw_player(stdscr)
        self.draw_entities(stdscr)
        self.draw_events(stdscr)

        key = stdscr.getch()
        if key != -1:  # -1 = aucune touche pressée
            self.input_system.process_input(
                key_to_action(key))  # traite l'entrée et la convertit en action que le système peut comprendre


        if key == ord('r'):
            self.univers.set_scene(world.Test)
        elif key == ord('n'):
            self.univers.set_scene(world.Test2)
        elif key == ord('s'):
            self.univers.set_scene(world.Test3)
        elif key == ord('m'):
            self.univers.mode_change("dialogue")


        self.univers.current_scene.event_system.update(self.univers.player, key_to_action(key))

    def dialogue_mode(self, stdscr):
        stdscr.addstr(0, 0, "C'est le mode dialogue ça !")
        key = stdscr.getch()
        if key == ord('m'):
            self.univers.mode_change("exploration")

    def show_scene(self, stdscr):
        scene = self.univers.current_scene
        for y, ligne in enumerate(scene.map_data):
            stdscr.addstr(y, 0, ligne)
        stdscr.addstr(len(scene.map_data)+1, 0, "Appuie sur 'q' pour quitter.")

    def draw_player(self, stdscr):
        player = self.univers.player
        y, x = player.position
        stdscr.addstr(y, x, player.sprite)

    def draw_entity(self, stdscr, entity):
        y, x = entity.position
        stdscr.addstr(y, x, entity.sprite)
    def draw_entities(self, stdscr):
        scene = self.univers.current_scene
        for entity in scene.entities:
            self.draw_entity(stdscr, entity)

    def draw_event(self, stdscr, event):
        y, x = event.position
        stdscr.addstr(y, x, event.sprite)
    def draw_events(self, stdscr):
        scene = self.univers.current_scene
        for event in scene.event_system.events.values():
            self.draw_event(stdscr, event)