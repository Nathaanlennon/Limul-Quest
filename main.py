import scripts.setup_environment #necessary to add more "extensions", does nothing else and the program works whitout it

from engine.ui.curses_ui import CursesUI
from engine.core.base import UniverseData
from world import Test


def main():
    data = UniverseData(Test, (20,71))  # size is the size with the map and interface, number of lines and columns
    interface = CursesUI(data)  # interface spécifique
    interface.run()  # démarre l'affichage


if __name__ == "__main__":
    main()
