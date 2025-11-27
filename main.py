import scripts.setup_environment #necessary to add more "extensions", does nothing else and the program works whitout it

from engine.ui.curses_ui import CursesUI
from engine.core.base import UniverseData
from world import Village1


def main():
    data = UniverseData(Village1,(20, 71))  # logique pure
    interface = CursesUI(data)  # interface spécifique
    interface.run()  # démarre l'affichage


if __name__ == "__main__":
    main()