from ui.curses_ui import CursesUI
from core.base import UniverseData
from world import Test


def main():
    data = UniverseData(Test)# logique pure
    interface = CursesUI(data)  # interface spécifique
    interface.run()        # démarre l'affichage

if __name__ == "__main__":
    main()
