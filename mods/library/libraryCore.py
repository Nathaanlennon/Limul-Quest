import os


SAVES_DIR = "saves"


class library:
    def __init__(self, universe = None):
        self.state = "beging"
        self.book = {
            1 : "Livre sort de feu",
            2 : "Livre sort d'eau",
            3 : "Livre sort de terre",
            4 : "Livre sort de vent"
        }
        self.universe = universe
        self.setup_accounts()
        self.current_account = ""
        self.active = False

    def extract_data(self):
        data = {
            "book" : self.book
        }
        return data

    def load_data(self, data):
        self.book.update(data["book"])

    def setup_accounts(self):
        universe_path = os.path.join(SAVES_DIR, "FishWorld")#self.universe.name
        players = [d for d in os.listdir(universe_path)
                   if os.path.isdir(os.path.join(universe_path, d))]
        for player in players:
            self.book[player] = 0
        #self.accounts[self.universe.player.name] = 0

    def set_current_account(self, name_account):
        if name_account in self.accounts:
            self.current_account = name_account
            self.active = True

    def transfert(self, montant):
        if montant <= self.universe.player.inventory.money:
            if self.state == "deposit":
                self.accounts[self.current_account] += montant
                self.universe.player.inventory.money -= montant
            elif self.state == "withdraw":
                self.accounts[self.universe.player.name] -= montant
                self.universe.player.inventory.money += montant
            self.active = False
            self.state = "final"


libraryManager = library()


def setup_libraryManger(universe):
    libraryManager.universe = universe