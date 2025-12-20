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
            input_type="int"
        )

    elif key == ord('j'):
        universe.mode_change("pendu")




def pendu(universe, key):



    if penduCore.levelChoice == 0 :
        def handleUserTry(num):
                if num>0 and num<4 :
                    penduCore.levelChoice = num
                    penduCore.chosenWord = penduCore.getRandomWord(num)
                    penduCore.wordBeingFound = penduCore.updateWord()

        universe.request_text_input(
                handleUserTry,
                prompt="Veuillez rentrer le niveau voulu (entre 1 et 3): ",
                input_type="int"
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
                        input_type="string"
                    )
        
        elif penduCore.mistakes == 6 :
           penduCore.hasLost = True
           time.sleep(2)
           universe.mode_change("exploration")
           penduCore.penduSpriteShowed = []
           penduCore.levelChoice = 0
           penduCore.chosenWord = ""
           penduCore.listWords = []
           penduCore.mistakes = 0
           penduCore.hasLost = False
           penduCore.lettersFound = []
           penduCore.wordBeingFound = ""


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

            elif libraryManager.state == "return":
                libraryManager.active = True

            elif libraryManager.state == "erreur":
                ...

    if libraryManager.active:
        universe.request_text_input(
            libraryManager.transfert,
            prompt = "Saisir le montant voulu : ",
            input_type = "int"
        )


input_modes = {
    # custom_input: custom_input,
    "debug": debug_input,
    "pendu":pendu,
    "bank": bank,
    "library": library,
}