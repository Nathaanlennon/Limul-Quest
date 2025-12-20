import os


SAVES_DIR = "saves"


class library:
    def __init__(self, universe = None):
        self.state = "beging"
        self.book_no_take = ["Livre de feu",
                             "Livre d'eau"]
        self.universe = universe
        self.current_account = "Tom"  #self.universe.player.name
        self.active = False
        self.accounts = {}
        self.setup_accounts()
        self.max = 2

    def init_universe(self, universe):
        self.universe = universe


    def extract_data(self):
        data = {
            "accounts": self.accounts
        }
        return data

    def load_data(self, data):
        self.accounts = data["accounts"]

    def setup_accounts(self):
        universe_path = os.path.join(SAVES_DIR, "FishWorld")#self.universe.name
        players = [d for d in os.listdir(universe_path)
                   if os.path.isdir(os.path.join(universe_path, d))]

        for player_name in players:
            self.accounts[player_name] = []

    def verification(self):
        return len(self.accounts[self.universe.player.name]) <= self.max #à définir

    def available_books(self):
        intersection = list(set(self.book_no_take) - set(self.accounts[self.universe.player.name]))
        return intersection


libraryManager = library()


def setup_libraryManger(universe):
    libraryManager.universe = universe