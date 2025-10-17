import curses
from core.world import *



class CursesUI:
    def __init__(self, univers):
        self.univers = univers

    def run(self):
        curses.wrapper(self.main_loop)

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)

        while True:
            stdscr.clear()
            self.afficher_scene(stdscr)
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.univers.set_scene(Test)
            elif key == ord('n'):
                self.univers.set_scene(Test2)
            elif key == ord('s'):
                self.univers.set_scene(Test3)

    def afficher_scene(self, stdscr):
        scene = self.univers.current_scene
        for y, ligne in enumerate(scene.map_data):
            stdscr.addstr(y, 0, ligne)
        stdscr.addstr(len(scene.map_data)+1, 0, "Appuie sur 'q' pour quitter.")