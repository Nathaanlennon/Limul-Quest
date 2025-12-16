import json
import random


# Ouvrir et charger le fichier JSON
with open("mods/penduProject/words.json", "r", encoding="utf-8") as f:
    data = json.load(f) 

levelChoice = 0
chosenWord = ""
listWords = []
mistakes = 0
hasLost = False
lettersFound = []
wordBeingFound = ""
penduSprite = [[
    "(_)",
],
[
    "(_)",
    "\| "
],
[
    "(_)",
    "\|/"
],
[
    "(_)",
    "\|/",
    " |"
],
[
    "(_)",
    "\|/",
    " |",
    "/   "
],
[
    "(_)",
    "\|/",
    " |",
    "/ \ "
],
]
penduSpriteShowed = []

def getRandomWord(level):
        listWords = data[level-1]
        randomNumber = random.randint(0,len(listWords)-1) 
        chosenWord = listWords[randomNumber]

        return chosenWord

def checkLetter(letter):
        if letter in chosenWord : 
               return letter
        else :
               return False
        
def updateWord():
    global wordBeingFound
    wordBeingFound = ""

    for trueLetters in chosenWord :
                if trueLetters in lettersFound :
                    wordBeingFound += trueLetters
                elif (trueLetters == "é") and ("e" in lettersFound) :
                    wordBeingFound += trueLetters
                elif (trueLetters == "â") and ("a" in lettersFound) :
                    wordBeingFound += trueLetters
                elif (trueLetters == "è") and ("e" in lettersFound) :
                    wordBeingFound += trueLetters
                else :
                    wordBeingFound += "_"
    return wordBeingFound
    
def appendLetters(letter): 
    lettersFound.append(letter)
    return updateWord()

def updateSprite():
      updatedSprite = penduSprite[mistakes-1]
      return updatedSprite