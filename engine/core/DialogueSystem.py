import json  # used to load dialogues from JSON files
import os    # used to check file paths

class DialogueSystem:
    """Manage dialogue flow for the game: loading dialogues, slicing text into chunks,
    handling choices, and advancing lines or branches."""
    def __init__(self, universe):
        # store reference to the game universe to trigger mode changes when dialogues end
        self.universe = universe
        # list of dialogue entries loaded from a JSON file
        self.dialogues = []
        # remaining text of the current dialogue line yet to be shown
        self.current_dialogue = ""
        # currently displayed chunk of text (up to max_length)
        self.current_reading = ""
        # state controls how the system behaves: NEXT_LINE, TEXT_CHUNK, CHOICE
        self.state = "NEXT_LINE"
        # list of visible choice texts for the current dialogue entry
        self.choices = []
        # index of the current dialogue entry in self.dialogues
        self.index = -1
        self.max_length = 100 #max size for now, will implement text wrapping later

    def check_requirements(self, require):
        """
        Vérifie si les conditions d'un dialogue ou d'une option sont remplies.

        ```
        require : dict
            Dictionnaire des conditions à vérifier. Les clés possibles :
            - 'player:<clé>' : vérifie self.universe.player.ext_data[clé] == valeur ou présence d'un item
            - 'universe:<clé>' : vérifie self.universe.ext_data[clé] == valeur
            - 'has_item:<item_id>' : vérifie que le joueur a au moins 1 de cet item
        """

        if not require or require == {}:
            return True  # pas de condition, toujours accessible

        for key, value in require.items():
            if key.startswith("player:"):
                subkey = key.split(":", 1)[1]
                # Vérifie item dans l'inventaire
                if subkey.startswith("has_item:"):
                    item_id = subkey.split(":", 1)[1]
                    if self.universe.player.inventory.get(item_id, 0) < 1:
                        return False
                else:
                    if self.universe.player.ext_data.get(subkey) != value:
                        return False
            elif key.startswith("universe:"):
                subkey = key.split(":", 1)[1]
                if self.universe.ext_data.get(subkey) != value:
                    return False
            elif key.startswith("has_item:"):
                item_id = key.split(":", 1)[1]
                if self.universe.player.inventory.get(item_id, 0) < 1:
                    return False
            else:
                # fallback : vérifie dans player.ext_data
                if self.universe.player.ext_data.get(key) != value:
                    return False
        return True

    def apply_effects(self, effects):
        """
        Applique les effets définis dans un dialogue ou une option.
        Anciennement `set_flag`, mais étendu pour inclure :
        - player:<clé> → modifie self.universe.player.ext_data
        - universe:<clé> → modifie self.universe.ext_data
        - give_item:<item_id> → ajoute un item à l'inventaire du joueur
        - remove_item:<item_id> → retire un item de l'inventaire du joueur
        """

        if not effects:
            return

        for key, value in effects.items():
            if key.startswith("player:"):
                subkey = key.split(":", 1)[1]
                self.universe.player.ext_data[subkey] = value
            elif key.startswith("universe:"):
                subkey = key.split(":", 1)[1]
                self.universe.ext_data[subkey] = value
            elif key.startswith("give_item:"):
                item_id = key.split(":", 1)[1]
                if int(value) > 0:
                    self.universe.player.add_to_inventory(item_id, int(value))
            elif key.startswith("remove_item:"):
                item_id = key.split(":", 1)[1]
                if int(value) < 0:
                    self.universe.player.remove_from_inventory(item_id, value)
            else:
                # Par défaut : stocke dans player.ext_data
                self.universe.player.ext_data[key] = value

    def set_dialogues(self, file_path):
        """Load dialogues from file_path if it exists, otherwise fall back to default.
        After loading, set the index to the first entry and prepare the current dialogue."""
        # check provided path exists and is a file
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # open and parse the JSON dialogues file
            with open(file_path, 'r') as file:
                self.dialogues = json.load(file)
        else:
            # fallback to default dialogues bundled with the project
            with open("assets/dialogues/default_dialogues.json", 'r') as file:
                self.dialogues = json.load(file)
        # start at the first dialogue entry
        self.index = 0
        # initialize current dialog state from the loaded dialogues
        self.set_current_dialogue()

    def set_current_dialogue(self):
        """Set self.current_dialogue and determine the next state based on length
        and presence of options for choice-based branching."""
        # only proceed if index is within bounds of the dialogues list
        if 0 <= self.index < len(self.dialogues):
            if self.check_requirements(self.dialogues[self.index].get("require", None)):
                # load the 'text' field of the current dialogue entry
                self.current_dialogue = self.dialogues[self.index]["text"]
                # if the text is longer than max_length, show it in chunks
                if len(self.current_dialogue) > self.max_length:
                     self.state = "TEXT_CHUNK"
                # if options exist, switch to CHOICE state and populate choices
                elif "options" in self.dialogues[self.index]:
                    self.state = "CHOICE"
                    self.set_choices()
                # prepare the first chunk of text to display (or the full text if short)
                #self.set_text_chunk()
            else:
                # requirements not met, skip to next line
                self.index += 1
                self.set_current_dialogue()

    def set_text_chunk(self):
        """Take the next chunk (up to max_length) from current_dialogue and assign it
        to current_reading. Update current_dialogue to contain remaining text."""
        # slice the next visible chunk
        self.current_reading = self.current_dialogue[:self.max_length]
        # remove the chunk from the remaining dialogue text
        self.current_dialogue = self.current_dialogue[self.max_length:]

        # if no remaining text, decide whether to present choices or move to next line
        if self.current_dialogue == "":
            if "options" in self.dialogues[self.index]:
                # if the current entry has options, switch to choice mode and populate them
                self.state = "CHOICE"
                self.set_choices()
            else:
                # otherwise signal that the system should proceed to the next dialogue line
                self.state = "NEXT_LINE"

    def set_choices(self):
        """Populate self.choices with the text of available options for the current entry."""
        # reset choices list
        self.choices = []
        # only proceed if the current entry defines options
        if "options" in self.dialogues[self.index]:
            # collect the display text for each option
            for choice in self.dialogues[self.index]["options"]:
                if self.check_requirements(choice.get("require", None)):
                    self.choices.append(choice["text"])

    def set_next_line(self, choice_index=None):
        """Advance the dialogue index. If currently in CHOICE state and a choice_index
        is provided, jump to the 'next' index specified by the chosen option.
        Otherwise, increment index to proceed linearly.
        After updating index, reset current reading and dialogue and either switch to
        exploration mode if dialogues are finished or prepare the next dialogue entry."""
        # if user made a choice, jump to the chosen branch index
        if self.state == "CHOICE" and choice_index is not None:
            # set index based on the 'next' field of the chosen option
            choice = self.dialogues[self.index]["options"][choice_index]
            self.index = choice["next"]
            if "effects" in choice:
                self.apply_effects(choice["effects"])

            # clear choices since we've taken a branch
            self.choices = []
            # prepare to load the next line
            self.state = "NEXT_LINE"
        else:
            # no choice made, move to the next sequential dialogue entry
            self.index += 1

        # clear current text buffers before loading the next entry
        self.current_dialogue = ""
        self.current_reading = ""
        # if index is out of range or set to -1, return to exploration mode in universe
        if self.index == -1 or self.index >= len(self.dialogues):
            # trigger mode change in the game to resume exploration
            self.universe.mode_change("exploration")
        else:
            # otherwise prepare the next dialogue entry
            self.set_current_dialogue()
