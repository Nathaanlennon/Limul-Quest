import os
os.chdir(os.path.dirname(__file__))
from engine.core.base import UniverseData
import engine.core.SaveManager as SaveManager





def main():
    universe_name = SaveManager.choose_universe()
    player_name = SaveManager.choose_player(universe_name)

        # Charger l'univers ici

    data = UniverseData("Monde1", (20 * 2, 71),
                        universe_name, player_name, (2,3))  # size is the size with the map and interface, number of lines and columns

    from engine.ui.curses_ui import CursesUI

    interface = CursesUI(data)  # interface spécifique
    interface.run()  # démarre l'affichage






if __name__ == "__main__":
    main()

