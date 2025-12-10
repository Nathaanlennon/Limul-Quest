import os


SAVES_DIR = "saves"


class Bank:
    def __init__(self, universe = None):
        self.state = "beging"
        self.accounts = {}
        self.universe = universe
        self.setup_accounts()
        self.current_account = ""
        self.active = False

    def extract_data(self):
        data = {
            "accounts" : self.accounts
        }
        return data

    def load_data(self, data):
        self.accounts.update(data["accounts"])

    def setup_accounts(self):
        universe_path = os.path.join(SAVES_DIR, "FishWorld")#self.universe.name
        players = [d for d in os.listdir(universe_path)
                   if os.path.isdir(os.path.join(universe_path, d))]
        for player in players:
            self.accounts[player] = 0
        #self.accounts[self.universe.player.name] = 0

    def set_current_account(self, name_account):
        if name_account in self.accounts:
            self.current_account = name_account
            self.active = True

    def transfert(self, montant):
        if self.state == "deposit":
            if montant <= self.universe.player.inventory.money:
                self.accounts[self.current_account] += montant
                self.universe.player.inventory.money -= montant
        elif self.state == "withdraw":
            if montant <= self.accounts[self.universe.player.name]:
                self.accounts[self.universe.player.name] -= montant
                self.universe.player.inventory.money += montant
        self.active = False


bankManager = Bank()


def setup_bankManger(universe):
    bankManager.universe = universe