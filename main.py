from core.game import Game
from ui.curses_ui import CursesUI
from core.world import UniversData
from core.InputSystem import *

def main():
    data = UniversData() # logique pure
    input_system = InputSystem(data)  # système d'entrée
    interface = CursesUI(data, input_system)  # interface spécifique
    interface.run()        # démarre l'affichage

if __name__ == "__main__":
    main()
