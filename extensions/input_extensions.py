#this module defines various input extension modes for the application.

#It is very simple to use : just add new modes to the `modes` dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.
#Each mode function should accept two parameters, typically the universe object and the key input, which is used for handling input in that mode.
#Note that the input is defined by a mapping from key codes to action strings in the engine/ui/curses_ui.py file.
#You can create your own mapping in ui_extensions.py if needed.
#exemple:
#def custom_input(universe, key):
#    # Custom input implementation

input_modes = {
    #custom_input: custom_input,
}