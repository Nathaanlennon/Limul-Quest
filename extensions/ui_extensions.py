#This module defines various UI extension modes for the application.

#It is very simple to use : just add new modes to the modes dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.

#Each mode function should accept a single parameter, typically the standard screen object (stdscr), which is used for rendering the UI in that mode.

#Example:
#def custom_mode(self, stdscr):
#    # Custom mode implementation
import time
import mods.penduProject.penduCore as penduCore
from mods.bank.bankCore import bankManager
import mods.bank.bankCore as bankCore
from mods.library.libraryCore import libraryManager
import mods.library.libraryCore as libraryCore
from engine.core.logging_setup import logger

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



def bank(self, stdscr):
    self.draw(stdscr, "scene", 1, 1, f"Argent en poche : {self.universe.player.inventory.money}")

    if not bankManager.active:
        if bankManager.state == "beging":
            self.draw(stdscr,"hud", 1,1, f"Bonjour, bienvenue chez Limulbank ! Que voulez-vous faire ?")
            self.draw(stdscr,"hud", 2,1, f"1 - Bonjour, j'aimerais déposer de l'argent, s'il vous plaît")
            self.draw(stdscr,"hud", 3,1, f"2 - Bonjour, je voudrais retirer de l'argent, s'il vous plaît")
            self.draw(stdscr,"hud", 4,1, f"3 - Bonjour, désolé je me suis trompé")

        elif bankManager.state == "deposit":
            self.draw(stdscr, "hud", 1, 1, f"Choisissez un compte")
            n = 0
            for key, value in bankManager.accounts.items():
                self.draw(stdscr, "hud", 2+n, 1, f"{key} : {value}")
                n += 1

        elif bankManager.state == "final":
            self.draw(stdscr, "hud", 1, 1, f"Merci, n'hésiter pas à revenir, bonne journée")

    else:
        if bankManager.state == "deposit":
            self.draw(stdscr, "hud", 1, 1, f"Compte choisi : {bankManager.current_account} {bankManager.accounts[bankManager.current_account]}")
            self.draw(stdscr, "hud", 2, 1, f"Combien voulez-vous déposer ?")

        if bankManager.state == ("withdraw"):
            self.draw(stdscr, "hud", 1, 1, f"{bankManager.universe.player.name} : {bankManager.accounts[bankManager.universe.player.name]}")
            self.draw(stdscr, "hud", 2, 1, f"Combien voulez-vous retirer ?")


def library(self, stdscr):
    if not libraryManager.active:
        if libraryManager.state == "beging":
            self.draw(stdscr,"hud", 1,1, f"Bonjour, bienvenue chez Libramul ! Que voulez-vous faire ?")
            self.draw(stdscr,"hud", 2,1, f"1 - Bonjour, j'aimerais emprunter un livre, s'il vous plaît")
            self.draw(stdscr,"hud", 3,1, f"2 - Bonjour, je viens rendre un livre, s'il vous plaît")
            self.draw(stdscr,"hud", 4,1, f"3 - Bonjour, désolé je me suis trompé")

        elif libraryManager.state == "borrow":
            self.draw(stdscr, "hud", 1, 1, f"Choisissez un livre :")
            n = 0
            for book in libraryManager.available_books():
                self.draw(stdscr, "hud", 2+n, 1, f"{book}")
                n += 1
            """
            if libraryManager.verification():
                self.draw(stdscr, "hud", 1, 1, f"Choisissez un livre :")
                n = 1
                for book in libraryManager.available_books():
                    self.draw(stdscr, "hud", 1 + n, 1, f"{n} : {book}")
                    n += 1
            """


ui_modes = {
    "bank": bank,
    "library": library,
    "pendu": pendu
    # cutom_mode: custom_mode,
}


# There is a key mapping in engine/ui/curses_ui.py that maps key codes to action strings.
# You can add more keys here if needed and even modify existing ones.
# Note that modifying existing keys may affect the default behavior of the application.


KEY_MAPPING = {
    # Example: ord('a'): "CUSTOM_ACTION",
}