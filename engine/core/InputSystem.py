import importlib.util
from engine.core.logging_setup import logger


if importlib.util.find_spec("extensions.input_extensions") is not None:
    import extensions.input_extensions as input_ext
    charged = True
else:
    logger.warning(f"Module 'extension/input_extensions' is missing. please import scripts/setup_environment.py. in the main")
    charged = False


def exploration_input(universe, key):
    if key == "UP":
        universe.player.move(-1, 0)  # Déplacer vers le haut
        universe.player.orientation = "UP"
    elif key == "DOWN":
        universe.player.move(1, 0)   # Déplacer vers le bas
        universe.player.orientation = "DOWN"
    elif key == "LEFT":
        universe.player.move(0, -1)  # Déplacer vers la gauche
        universe.player.orientation = "LEFT"
    elif key == "RIGHT":
        universe.player.move(0, 1)   # Déplacer vers la droite
        universe.player.orientation = "RIGHT"

    elif key == "TEST":
        universe.mode_change("test")



    elif key == "INTERACT":
        ...

    universe.current_scene.event_system.update(universe.player, key)

def dialogue_input(universe, key):
    if universe.dialogue_system.state == "TEXT_CHUNK":
        if key == "INTERACT":
            universe.dialogue_system.set_text_chunk()
    elif universe.dialogue_system.state == "CHOICE":
        if isinstance(key, int):  # renvoie d'un chiffre via le mapping
            if 1 <= key <= len(universe.dialogue_system.choices):
                universe.dialogue_system.set_next_line(choice_index=key - 1)

    elif universe.dialogue_system.state == "NEXT_LINE":
        if key == "INTERACT":
            universe.dialogue_system.set_next_line()

def inventory_input(universe, key):
    if key == ord('v'):
        universe.mode_change("exploration")

modes = {
    "exploration": exploration_input,
    "dialogue": dialogue_input,
    "inventory": inventory_input
}

if charged:
    modes.update(input_ext.input_modes)

