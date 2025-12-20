# this module defines various input extension modes for the application.

# It is very simple to use : just add new modes to the modes dictionary, where the key is the mode name and the value is the corresponding function that implements the mode's behavior.
# Each mode function should accept two parameters, typically the universe object and the key input, which is used for handling input in that mode.
# Note that the input is defined by a mapping from key codes to action strings in the engine/ui/curses_ui.py file.
# You can create your own mapping in ui_extensions.py if needed.

import time
from engine.core.logging_setup import logger
from engine.core.CombatSystem import combat_system
import mods.penduProject.penduCore as penduCore
from mods.bank.bankCore import bankManager
from mods.library.libraryCore import libraryManager

# exemple:
# def custom_input(universe, key):
#    # Custom input implementation
def test(universe, key):
    if key == "INTERACT":
        universe.mode_change("exploration")

def debug_input(universe, key):
    if key == "DEBUG":  # debug key is W
        universe.mode_change("exploration")
        # TODO: remove debug keys

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
            input_type="int",

        )

    elif key == ord('j'):
        universe.mode_change("pendu")




def pendu(universe, key):

    if penduCore.levelChoice == 0 :
        def handleUserTry(num):
                if 0 < num < 4:
                    penduCore.levelChoice = num
                    penduCore.chosenWord = penduCore.getRandomWord(num)
                    penduCore.wordBeingFound = penduCore.updateWord()

        universe.request_text_input(
                handleUserTry,
                prompt="Veuillez rentrer le niveau voulu (entre 1 et 3): ",
                input_type="int",
                x = 2,
                y = 1
            )
        
    if penduCore.chosenWord != "" :

        if penduCore.mistakes < 6 : 
                
                def handleUserTry(letter):
                 if not (len(letter) > 1) and letter!= "" :

                    checkedLetter = penduCore.checkLetter(letter) # fonction qui renvoi la lettre si dans le mot false sinon, 
                    #si lettre on push si false on ajoute 1 à mistakes
                    if checkedLetter == False :

                        penduCore.mistakes +=1
                        penduCore.wordBeingFound = penduCore.updateWord()
                        penduCore.penduSpriteShowed = penduCore.updateSprite()
                    else :

                        penduCore.wordBeingFound = penduCore.appendLetters(checkedLetter)

                universe.request_text_input(
                        handleUserTry,
                        prompt="Veuillez rentrer une lettre du mot : ",
                        input_type="string",
                        y = 5,
                        x = 1
                    )

                if penduCore.wordBeingFound == penduCore.chosenWord :

                    penduCore.hasWon = True

                    def handleUserHasWon(letter):
                            if letter == "Y" or letter =="y" :
                                universe.player.inventory.money +=1*penduCore.levelChoice
                                penduCore.resetStats()


                            elif letter == "N" or letter == "n"  :
                                universe.player.inventory.money +=1*penduCore.levelChoice
                                penduCore.resetStats()
                                universe.mode_change("exploration")
                                


                    universe.request_text_input(
                            handleUserHasWon,
                            prompt="Voulez vous recommencer ? (Y/N) : ",
                            input_type="string",
                            x = 1,
                            y = 1
                        )

        
        elif penduCore.mistakes >= 6 :
           penduCore.hasLost = True
           
           def handleUserHasLost(letter):
                 if letter == "Y" or letter == "y" :
                    penduCore.resetStats()

                 elif letter == "N" or letter == "n"  :
                    penduCore.resetStats()
                    universe.mode_change("exploration")
                     


           universe.request_text_input(
                handleUserHasLost,
                prompt="Voulez vous recommencer ? (Y/N) : ",
                input_type="string",
                x = 1,
                y = 1
            )


def bank(universe, key):
    if not bankManager.active:
        if bankManager.state == "beging":
            if key == 1:
                bankManager.state = "deposit"

            elif key == 2:
                bankManager.state = "withdraw"

            elif key == 3:
                bankManager.state = "erreur"

        elif bankManager.state == "deposit":
            universe.request_text_input(
                bankManager.set_current_account,
                prompt="Nom du compte voulu : ",
                input_type="string"
            )

        elif bankManager.state == "withdraw":
            bankManager.active = True

        elif bankManager.state == "erreur":
            ...

        elif bankManager.state == "final":
            bankManager.active = False
            bankManager.state = "beging"
            universe.mode_change("exploration")

    if bankManager.active:
        universe.request_text_input(
            bankManager.transfert,
            prompt="Saisir le montant voulu : ",
            input_type="int"
        )


def library(universe, key):
    if not libraryManager.active:
        if libraryManager.state == "beging":
            if key == 1:
                libraryManager.state = "borrow"

            elif key == 2:
                libraryManager.state = "return"

            elif key == 3:
                libraryManager.state = "erreur"

        elif libraryManager.state == "borrow":
            if libraryManager.verification():
                universe.request_text_input(
                    libraryManager.select_book,
                    prompt = "Numéro du livre voulu : ",
                    input_type = "int"
                )
            else:
                libraryManager.state = "final"

        elif libraryManager.state == "return":
            if libraryManager.verification():
                universe.request_text_input(
                    libraryManager.select_book,
                    prompt = "Numéro du livre à rendre : ",
                    input_type = "int",
                )
            else:
                libraryManager.state = "final"

        elif libraryManager.state == "erreur":
            libraryManager.active = False
            libraryManager.state = "beging"
            universe.mode_change("exploration")

        elif libraryManager.state == "final":
            libraryManager.active = False
            libraryManager.state = "beging"
            universe.mode_change("exploration")

    if libraryManager.active:
        universe.request_text_input(
            libraryManager.borrowing,
            prompt="(o:oui / n:non) : ",
            input_type="string"
        )


input_modes = {
    # custom_input: custom_input,
    "debug": debug_input,
    "pendu":pendu,
    "bank": bank,
    "library": library,
}