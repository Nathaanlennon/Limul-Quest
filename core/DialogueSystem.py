import json
import os

class DialogueSystem:
    def __init__(self, universe):
        self.universe = universe
        self.dialogues = []
        self.current_dialogue = ""
        self.current_reading = ""
        self.state = "NEXT_LINE"
        self.choices = []
        self.index = -1
        self.max_length = 100 #max size for now, will implement text wrapping later


    def set_dialogues(self, file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                self.dialogues = json.load(file)
        else:
            with open("assets/dialogues/default_dialogues.json", 'r') as file:
                self.dialogues = json.load(file)
        self.index = 0
        self.set_current_dialogue()

    def set_current_dialogue(self):
        if 0 <= self.index < len(self.dialogues):
            self.current_dialogue = self.dialogues[self.index]["text"]
            if len(self.current_dialogue) > self.max_length:
                self.state = "TEXT_CHUNK"
            elif "options" in self.dialogues[self.index]:
                self.state = "CHOICE"
                self.set_choices()
            self.set_text_chunk()

    def set_text_chunk(self):
        self.current_reading = self.current_dialogue[:self.max_length]
        self.current_dialogue = self.current_dialogue[self.max_length:]

        if self.current_dialogue == "":
            if "options" in self.dialogues[self.index]:
                self.state = "CHOICE"
                self.set_choices()
            else:
                self.state = "NEXT_LINE"

    def set_choices(self):
        self.choices = []
        if "options" in self.dialogues[self.index]:
            for choice in self.dialogues[self.index]["options"]:
                self.choices.append(choice["text"])

    def set_next_line(self, choice_index=None):
        if self.state == "CHOICE" and choice_index is not None:
            self.index = self.dialogues[self.index]["options"][choice_index]["next"]
            self.choices = []
            self.state = "NEXT_LINE"
        else:
            self.index += 1

        self.current_dialogue = ""
        self.current_reading = ""
        if self.index == -1 or self.index >= len(self.dialogues):
            self.universe.mode_change("exploration")
        else:
            self.set_current_dialogue()



