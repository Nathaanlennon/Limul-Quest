from core.InputSystem import InputSystem
from ui.curses_ui import CursesUI
from core.base import UniversData
from world import Test


def main():
    data = UniversData(Test) # logique pure
    input_system = InputSystem(data)  # système d'entrée
    interface = CursesUI(data, input_system)  # interface spécifique
    interface.run()        # démarre l'affichage

if __name__ == "__main__":
    main()
