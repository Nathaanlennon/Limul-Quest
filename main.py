import os
os.chdir(os.path.dirname(__file__))
from engine.core.base import UniverseData
from engine.core.logging_setup import logger


import os

SAVES_DIR = "saves"

def choose_universe():
    if not os.path.exists(SAVES_DIR):
        os.makedirs(SAVES_DIR)

    universes = [d for d in os.listdir(SAVES_DIR)
                 if os.path.isdir(os.path.join(SAVES_DIR, d))]

    print("Available universes:")
    for i, u in enumerate(universes, start=1):
        print(f"{i}. {u}")
    print("0. Create new universe")

    choice = input("Select a universe: ").strip()
    if choice == "0":
        new_universe = input("Enter new universe name: ").strip()
        universe_path = os.path.join(SAVES_DIR, new_universe)
        os.makedirs(universe_path, exist_ok=True)
        return new_universe
    else:
        try:
            index = int(choice) - 1
            return universes[index]
        except (ValueError, IndexError):
            print("Invalid choice, try again.")
            return choose_universe()


def choose_player(universe_name):
    universe_path = os.path.join(SAVES_DIR, universe_name)
    players = [d for d in os.listdir(universe_path)
               if os.path.isdir(os.path.join(universe_path, d))]

    print(f"Available players in '{universe_name}':")
    for i, p in enumerate(players, start=1):
        print(f"{i}. {p}")
    print("0. Create new player")

    choice = input("Select a player: ").strip()
    if choice == "0":
        new_player = input("Enter new player name: ").strip()
        player_path = os.path.join(universe_path, new_player)
        os.makedirs(player_path, exist_ok=True)
        return new_player
    else:
        try:
            index = int(choice) - 1
            return players[index]
        except (ValueError, IndexError):
            print("Invalid choice, try again.")
            return choose_player(universe_name)




def main():
    universe_name = choose_universe()
    player_name = choose_player(universe_name)

        # Charger l'univers ici

    data = UniverseData("Monde1", (20 * 2, 71),
                        name=universe_name, player=player_name)  # size is the size with the map and interface, number of lines and columns

    from engine.ui.curses_ui import CursesUI

    interface = CursesUI(data)  # interface spécifique
    interface.run()  # démarre l'affichage






if __name__ == "__main__":
    main()

