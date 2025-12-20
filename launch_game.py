import engine.core.SaveManager as SaveManager
import subprocess
import sys
import os

def main():
    universe_name = SaveManager.choose_universe()
    player_name = SaveManager.choose_player(universe_name)

    # Chemin vers main.py (même répertoire)
    script_path = os.path.join(os.path.dirname(__file__), "main.py")

    # Lancement du script avec arguments
    subprocess.run([
        sys.executable,   # python utilisé pour lancer CE script
        script_path,
        universe_name,
        player_name
    ])

if __name__ == "__main__":
    main()
