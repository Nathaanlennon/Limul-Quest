#this module defines various input extension modes for the application.

#It is very simple to use : just add new modes to the `modes` dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.
#Each mode function should accept two parameters, typically the universe object and the key input, which is used for handling input in that mode.
#Note that the input is defined by a mapping from key codes to action strings in the engine/ui/curses_ui.py file.
#You can create your own mapping in ui_extensions.py if needed.

from engine.core.logging_setup import logger
from engine.core.CombatSystem import combat_system
import conteur as conteur

#exemple:
#def custom_input(universe, key):
#    # Custom input implementation
def test(universe, key):
    if key == "INTERACT":
        universe.mode_change("exploration")

def debug_input(universe, key):

    if key == "DEBUG":
        universe.mode_change("exploration")
        # TODO: remove debug keys
    if key == ord('r'):
        universe.set_world("Monde1")
    elif key == ord('n'):
        universe.set_world("Monde2")
    elif key == ord('y'):
        universe.set_world("Monde3")
    elif key == ord('p'):
        universe.mode_change("exploration")
    elif key == ord('o'):
        universe.player.inventory.add_item("health_potion", 10)
        universe.player.inventory.add_item("bomb", 5)
        universe.player.inventory.money += 100
    elif key == ord('l'):
        universe.mode_change("inventory")
    elif key == 'TEST':
        universe.mode_change("exploration")
    elif key == ord('b'):
        universe.mode_change("combat")
        combat_system.add_fighter("goblin")
        combat_system.add_fighter("goblin")
    elif key == ord('c'):
        universe.player.save_save()
    elif key == ord('v'):
        universe.player.load_player()
    elif key == ord('t'):
        universe.save_save()
    elif key == ord('g'):
        universe.load_save()
    elif key == ord('£'):
        universe.scenes[universe.current_world].remove_all_entities()
    elif key == ord('h'):
        def handle_int(num):
            logger.info(f"User entered: {num}")

        universe.request_text_input(
            handle_int,
            prompt="Enter a number: ",
            input_type="int"
        )
    elif key == ord('j'):
        universe.mode_change("mode1")

def mode1(universe, key):
    if key == "INTERACT":
        conteur.a+=1

input_modes = {
    #custom_input: custom_input,
    "debug":debug_input,
    "mode1":mode1
}