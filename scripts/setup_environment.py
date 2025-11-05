import os

# Dossiers obligatoires
required_dirs = [
    "extensions"
]

for d in required_dirs:
    os.makedirs(d, exist_ok=True)

# Fichier d’input system par défaut
input_file = "extensions/ui_extensions.py"
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as f:
        f.write("""#This module defines various UI extension modes for the application.

#It is very simple to use : just add new modes to the `modes` dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.

#Each mode function should accept a single parameter, typically the standard screen object (`stdscr`), which is used for rendering the UI in that mode.

#Example:
#def custom_mode(stdscr):
#    # Custom mode implementation

modes = {
    #cutom_mode: custom_mode,
}

# There is a key mapping in engine/ui/curses_ui.py that maps key codes to action strings.
# You can add more keys here if needed and even modify existing ones.
# Note that modifying existing keys may affect the default behavior of the application.

KEY_MAPPING = {
    # Example: ord('a'): "CUSTOM_ACTION",
}
""")
input_file = "extensions/input_extensions.py"
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as f:
        f.write("""#this module defines various input extension modes for the application.

#It is very simple to use : just add new modes to the `modes` dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.
#Each mode function should accept two parameters, typically the universe object and the key input, which is used for handling input in that mode.
#Note that the input is defined by a mapping from key codes to action strings in the engine/ui/curses_ui.py file.
#You can create your own mapping in ui_extensions.py if needed.
#exemple:
#def custom_input(universe, key):
#    # Custom input implementation

modes = {
    #custom_input: custom_input,
}""")

input_file= "extensions/data_extensions.py"
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as f:
        f.write("""# this is where all the additionnal data will be put, all the data that is not originally in the game-engine. 
# It will be imported in the universe_data and the player_data in the core but the said core will never know nor use it, it's only for your additional extensions that you make

universe_data = {
    
}

player_data = {
    
}""")