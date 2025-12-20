import os
os.chdir(os.path.dirname(__file__))
from engine.core.base import UniverseData
import engine.core.SaveManager as SaveManager
import sys





def main():
    universe_name = sys.argv[1]
    player_name = sys.argv[2]

        # Charger l'univers ici

    data = UniverseData("Village1", (20 * 2, 71),
                        universe_name, player_name, (10,35  ))  # size is the size with the map and interface, number of lines and columns

    from engine.ui.curses_ui import CursesUI

    interface = CursesUI(data)  # interface spécifique
    interface.run()  # démarre l'affichage






if __name__ == "__main__":
    main()

