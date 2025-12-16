#This module defines various UI extension modes for the application.

#It is very simple to use : just add new modes to the `modes` dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.

#Each mode function should accept a single parameter, typically the standard screen object (`stdscr`), which is used for rendering the UI in that mode.

#Example:
#def custom_mode(self, stdscr):
#    # Custom mode implementation
import time
import mods.penduProject.penduCore as penduCore

def pendu(self, stdscr):
    if penduCore.hasLost == False :
        self.draw(stdscr,"hud", 1,1, f"Bonjour et bienvenue au pendu !")
        if penduCore.levelChoice !=0 :
            self.draw(stdscr,"hud", 2,1, f"Le niveau choisi est  : {penduCore.levelChoice}")
            self.draw(stdscr,"hud", 3,1, f"Pour debug : {penduCore.chosenWord}")
            self.draw(stdscr,"hud", 4,1, f"Nombre de chances restantes  : {6 -penduCore.mistakes}")
            self.draw(stdscr,"hud", 5,1, f"Le mot à deviner est : {penduCore.wordBeingFound}")    
    else :
            stdscr.clear()
            self.draw(stdscr,"hud", 10,10, f"Vous avez perdu !")
            penduCore.hasLost = False

    position = self.screens["scene"]["size"][1] // 2
    pilotiSprite, (maxx, maxy) = self.load_sprite("mods/penduProject/pilotiSprite.txt")
    self.draw_sprite("scene", pilotiSprite, 1,position - maxx//2, stdscr)
    self.draw_sprite("scene", penduCore.penduSpriteShowed, 9,24, stdscr)

ui_modes = {
    "pendu": pendu
    #cutom_mode: custom_mode,
}

# There is a key mapping in engine/ui/curses_ui.py that maps key codes to action strings.
# You can add more keys here if needed and even modify existing ones.
# Note that modifying existing keys may affect the default behavior of the application.

KEY_MAPPING = {
    # Example: ord('a'): "CUSTOM_ACTION",
}
