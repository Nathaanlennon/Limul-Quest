import os
os.chdir(os.path.dirname(__file__))
from engine.ui.curses_ui import CursesUI
from engine.core.base import UniverseData
from world import Test



def main():
    data = UniverseData("Monde1", (20*2,71), "Monde1")  # size is the size with the map and interface, number of lines and columns
    interface = CursesUI(data)  # interface spécifique
    interface.run()  # démarre l'affichage


if __name__ == "__main__":
    main()
