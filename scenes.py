class SceneOne:
    def draw(self, stdscr):
        stdscr.addstr(2, 5, "=== SCÈNE 1 ===")
        stdscr.addstr(4, 5, "→ pour passer à la scène 2.")
        stdscr.addstr(6, 5, "q pour quitter.")

class SceneTwo:
    def draw(self, stdscr):
        stdscr.addstr(2, 5, "=== SCÈNE 2 ===")
        stdscr.addstr(4, 5, "← pour revenir à la scène 1.")
        stdscr.addstr(6, 5, "q pour quitter.")
