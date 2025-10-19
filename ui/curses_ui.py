import curses
from core.world import *


def key_to_action(key):
    mapping = {
        ord('z'): "UP",
        ord('s'): "DOWN",
        ord('q'): "LEFT",
        ord('d'): "RIGHT",
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

    def run(self):
        curses.wrapper(self.main_loop)

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)

        while True:
            stdscr.clear()
            self.show_scene(stdscr)
            self.draw_player(stdscr)
            stdscr.refresh()

            key = stdscr.getch()
            if key != -1:  # -1 = aucune touche pressée
                self.input_system.process_input(key_to_action(key)) # traite l'entrée et la convertit en action que le système peut comprendre
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.univers.set_scene(Test)
            elif key == ord('n'):
                self.univers.set_scene(Test2)
            elif key == ord('s'):
                self.univers.set_scene(Test3)

    def show_scene(self, stdscr):
        scene = self.univers.current_scene
        for y, ligne in enumerate(scene.map_data):
            stdscr.addstr(y, 0, ligne)
        stdscr.addstr(len(scene.map_data)+1, 0, "Appuie sur 'q' pour quitter.")

    def draw_player(self, stdscr):
        player = self.univers.player
        y, x = player.position
        stdscr.addstr(y, x, player.sprite)