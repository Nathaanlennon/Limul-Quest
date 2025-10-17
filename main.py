from core.game import Game
from ui.curses_ui import CursesUI
from core.world import UniversData

def main():
    data = UniversData()        # logique pure
    interface = CursesUI(data)  # interface spécifique
    interface.run()        # démarre l'affichage

if __name__ == "__main__":
    main()
