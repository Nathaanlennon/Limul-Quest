import random


class Saucisse:
    def __init__(self):
        self.length = 0
        self.universe = None  # This will be set when the instance is added to the universe

    def extract_data(self):
        return {
            "length": self.length,
            "test": "oui" if self.universe else "non"
        }
    def load_data(self, data):
        self.length = data["length"]



saucisse = Saucisse()# set universe for instances