import curses
import world
import os
from engine.core.logging_setup import logger
from engine.core.ItemManager import get_item



if os.path.exists("extensions/ui_extensions.py") and os.path.isfile("extensions/ui_extensions.py"):
    import extensions.ui_extensions as ui_ext
    charged = True
else:
    logger.warning(f"Module 'extensions/ui_extensions' is missing. Please run setup_environment.py in the engine")
    charged = False

curses.initscr()

# Table de correspondance Unicode -> curses ACS
CHAR_MAP = {
    '─': curses.ACS_HLINE,
    '│': curses.ACS_VLINE,
    '┌': curses.ACS_ULCORNER,
    '┐': curses.ACS_URCORNER,
    '└': curses.ACS_LLCORNER,
    '┘': curses.ACS_LRCORNER,
    '┬': curses.ACS_TTEE,
    '┴': curses.ACS_BTEE,
    '├': curses.ACS_LTEE,
    '┤': curses.ACS_RTEE,
    '┼': curses.ACS_PLUS,
}

# mapping global, créé une seule fois
KEY_MAPPING = {
    ord('z'): "UP", ord('Z'): "UP",
    ord('s'): "DOWN", ord('S'): "DOWN",
    ord('q'): "LEFT", ord('Q'): "LEFT",
    ord('d'): "RIGHT", ord('D'): "RIGHT",
    ord('e'): "INTERACT", ord('E'): "INTERACT",
    27 : "ESCAPE",  # ESCAPE key
    ord('x'): "QUIT", ord('X'): "QUIT",
    ord('w'): "TEST", ord('W'): "TEST",
    ord('i'): "INVENTORY", ord('I'): "INVENTORY",
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
}

# chiffres 0-9 → renvoie directement l'entier
for i in range(10):
    KEY_MAPPING[ord(str(i))] = i


def key_to_action(key):
    return KEY_MAPPING.get(key, key)


class CursesUI:
    def __init__(self, universe):
        self.universe = universe
        self.modes = {
            "exploration": self.exploration_mode,
            "dialogue": self.dialogue_mode,
            "inventory": self.inventory_mode,
            "debug": self.debug_mode,
            "combat": self.combat_mode
        }

        if charged:
            self.modes.update(ui_ext.ui_modes)

        self.mode_draw_function = self.modes[universe.mode]
        self.universe.set_mode_change_callback(self.change_mode)




    def run(self):
        curses.wrapper(self.main_loop)

    def change_mode(self, mode):
        self.mode_draw_function = self.modes.get(mode, self.exploration_mode)

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)  # getch make things waiting | edit I have no idea wtf this means


        while True:
            stdscr.erase()

            if stdscr.getmaxyx()[0] <= self.universe.size[0] or stdscr.getmaxyx()[1] <= self.universe.size[1]:
                stdscr.addstr(0, 0, "Veuillez agrandir la fenêtre")

            else:
                self.mode_draw_function(stdscr)
                #self.draw_screen(stdscr)
                key = stdscr.getch()
                stdscr.addstr(10, 10, f"Mode: {key}")
                self.universe.input_system(self.universe, key_to_action(
                    key))  # traite l'entrée et la convertit en action que le système peut comprendre



            stdscr.refresh()


    # modes de "gameplay"

    def exploration_mode(self, stdscr):
        self.show_scene(stdscr)
        self.draw_player(stdscr)
        self.draw_entities(stdscr)
        # self.draw_events(stdscr) # events dont have sprite for now

    def dialogue_mode(self, stdscr):
        stdscr.addstr(0, 0, self.universe.dialogue_system.current_reading)
        if self.universe.dialogue_system.state == "CHOICE":
            for idx, choice in enumerate(self.universe.dialogue_system.choices):
                stdscr.addstr(idx + 2, 0, f"{idx + 1}. {choice}")

    def inventory_mode(self, stdscr):
        stdscr.addstr(0, 0, "Inventory:")
        for idx, (item_name, quantity) in enumerate(self.universe.player.inventory.items()):
            item = get_item(item_name)
            stdscr.addstr(idx + 2, 0, f"{item['name']} x{quantity}")

    def combat_mode(self, stdscr):
        combat_system = self.universe.combat_system
        # TODO: changer la variable là qui se fait à chaque itération, ça sert à rien bordel
        stdscr.addstr(0, 0, "COMBAT MODE")
        for idx, enemy in enumerate(self.universe.combat_system.fighters):
            stdscr.addstr(idx + 2, 0, f"{enemy.name} - HP: {enemy.hp}")
        stdscr.addstr(10, 0, "Player HP: {}".format(self.universe.player.hp))

        q0 = combat_system.queue[0] if combat_system.queue else ""

        if combat_system.state == "START":
            stdscr.addstr(12, 0, "A wild enemy appears!")
        elif combat_system.state == "PLAYER_TURN":
            if q0 == "PLAYER_CHOICE":
                stdscr.addstr(12, 0, "Choose your action:")
                stdscr.addstr(13, 0, "1. Attack")
                stdscr.addstr(14, 0, "2. Ability")
                stdscr.addstr(15, 0, "3. Use Item")
            elif q0 == "ABILITY_CHOICE":
                stdscr.addstr(12, 0, "Choose your ability:")
                stdscr.addstr(13, 0, "0. Back")
                for idx, ability in enumerate(self.universe.player.ext_data["abilities"].values()):
                    stdscr.addstr(14 + idx, 0, f"{idx + 1}. {ability['name']}")
            elif q0 == "ITEM_CHOICE":
                stdscr.addstr(12, 0, "Choose your item:")
                stdscr.addstr(13, 0, "0. Back")
                inventory_items = list(self.universe.player.inventory.keys())
                for idx, item_name in enumerate(inventory_items):
                    item_data = get_item(item_name)
                    quantity = self.universe.player.inventory[item_name]
                    if quantity > 0 and item_data["type"] == "consumable":
                        stdscr.addstr(14 + idx, 0, f"{idx + 1}. {item_data['name']} x{quantity}")
            elif q0 == "CHOOSE_TARGET":
                stdscr.addstr(12, 0, "Choose your target:")
                stdscr.addstr(13, 0, "0. Back")
                for idx, enemy in enumerate(combat_system.fighters):
                    stdscr.addstr(14 + idx, 0, f"{idx + 1}. {enemy.name}")
            elif q0:
                    stdscr.addstr(12, 0, q0)


        elif combat_system.state == "ENEMIES_TURN" and q0:
                stdscr.addstr(12, 0, q0)
        elif combat_system.state == "VICTORY":
            stdscr.addstr(12, 0, "You won the combat!")
            stdscr.addstr(13, 0, "Loot:")
            for idx, (item_id, quantity) in enumerate(combat_system.loot):
                item = get_item(item_id)
                stdscr.addstr(14 + idx, 0, f"{item['name']} x{quantity}")



    def debug_mode(self, stdscr):
        self.exploration_mode(stdscr)
        stdscr.addstr(0, 0, "DEBUG MODE")




    def show_scene(self, stdscr):
        scene = self.universe.current_scene
        for y, ligne in enumerate(scene.map_data):
            stdscr.addstr(y, 0, ligne)

    def draw_player(self, stdscr):
        player = self.universe.player
        y, x = player.position
        stdscr.addstr(y, x, player.sprite)

    def draw_entity(self, stdscr, entity):
        y, x = entity.position
        stdscr.addstr(y, x, entity.sprite)

    def draw_entities(self, stdscr):
        scene = self.universe.current_scene
        for entity in scene.entities.values():
            self.draw_entity(stdscr, entity)

    def draw_event(self, stdscr, event):
        y, x = event.position
        stdscr.addstr(y, x, event.sprite)

    def draw_events(self, stdscr):
        scene = self.universe.current_scene
        for event in scene.event_system.events.values():
            self.draw_event(stdscr, event)

    def draw_screen(self, stdscr):
        h, w = self.universe.size


        # Bordures
        stdscr.addstr(0, 0, '┌' + '─' * (w - 2) + '┐')
        stdscr.addstr(h - 1, 0, '└' + '─' * (w - 2) + '┘')

        # Barre du milieu
        mid = h // 2
        stdscr.addstr(mid, 0, '├' + '─' * (w - 2) + '┤')

        # Bordures latérales sans remplir
        for y in range(1, h - 1):
            if y != mid:  # on saute la ligne centrale déjà dessinée
                stdscr.addstr(y, 0, '│')
                stdscr.addstr(y, w - 1, '│')

    def draw_text(self, stdscr, text, y, x):
        for idx, char in enumerate(text):
            if char in CHAR_MAP:
                stdscr.addch(y, x + idx, CHAR_MAP[char])
            else:
                stdscr.addch(y, x + idx, char)