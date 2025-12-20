import os
from engine.core.ItemManager import get_item_part


SAVES_DIR = "saves"


class library:
    def __init__(self, universe = None):
        self.state = "beging"
        self.book_no_take = ["fire_book",
                             "water_book",
                             "earth_book",]
        self.universe = universe
        self.active = False
        self.accounts = {}
        self.max = 2
        self.intersection = []
        self.selected_book =""
        self.index_book = 0

    def init_universe(self, universe):
        self.universe = universe
        self.current_account = self.universe.player.name
        self.setup_accounts()
        self.available_books()


    def extract_data(self):
        data = {
            "accounts": self.accounts
        }
        return data

    def load_data(self, data):
        self.accounts = data["accounts"]

    def setup_accounts(self):
        universe_path = os.path.join(SAVES_DIR, self.universe.name)
        players = [d for d in os.listdir(universe_path)
                   if os.path.isdir(os.path.join(universe_path, d))]

        for player_name in players:
            self.accounts[player_name] = []

    def verification(self):
        if self.state == "borrow":
            return len(self.accounts[self.universe.player.name]) <= self.max #à définir
        elif self.state == "return":
            return len(self.accounts[self.universe.player.name]) > 0

    def available_books(self):
        self.intersection = list(set(self.book_no_take) - set(self.accounts[self.universe.player.name]))

    def select_book(self, book):
        if self.state == "borrow":
            if 0 < book <= len(self.intersection):
                self.index_book = book - 1
                self.selected_book = self.intersection[self.index_book]
                self.active = True
        elif self.state == "return":
            if 0 < book <= len(self.accounts[self.universe.player.name]):
                self.index_book = book - 1
                self.selected_book = self.accounts[self.universe.player.name][self.index_book]
                self.active = True

    def borrowing(self, validation):
        if validation == 'o':
            if libraryManager.state == "borrow":
                self.intersection.pop(self.index_book)
                self.accounts[self.universe.player.name].append(self.selected_book)
            elif libraryManager.state == "return":
                self.accounts[self.universe.player.name].pop(self.index_book)
                self.intersection.append(self.selected_book)
            self.state = "final"
            self.active = False
        elif validation == 'n':
            self.active = False


libraryManager = library()


def setup_libraryManger(universe):
    libraryManager.universe = universe