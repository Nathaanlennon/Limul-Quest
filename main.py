from engine.ui.curses_ui import CursesUI
from engine.core.base import UniverseData
from world import Test


import os

# Dossiers obligatoires
required_dirs = [
    "game/data",
    "game/input",
    "game/worlds",
]

for d in required_dirs:
    os.makedirs(d, exist_ok=True)

# Fichier d’input system par défaut
input_file = "game/input/input_system.py"
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(
            "class CustomInputSystem:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def get_input(self):\n"
            "        return None\n"
        )



def main():
    data = UniverseData(Test)# logique pure
    interface = CursesUI(data)  # interface spécifique
    interface.run()        # démarre l'affichage

if __name__ == "__main__":
    main()
