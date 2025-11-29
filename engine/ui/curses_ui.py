import curses
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
    '£': '' # when a caracter takes 2 spaces, it fucks the rendering and the collisions so £ create a collision for the remaining space and the '' makes the space invisible. Please add £ after any 2 space taking caracter in your maps
}

# mapping global, créé une seule fois
KEY_MAPPING = {
    ord('Z'): "UP", ord('z'): "UP",
    ord('S'): "DOWN", ord('s'): "DOWN",
    ord('Q'): "LEFT", ord('q'): "LEFT",
    ord('D'): "RIGHT", ord('d'): "RIGHT",
    ord('E'): "INTERACT", ord('e'): "INTERACT",
    27: "ESCAPE",  # ESCAPE key
    ord('X'): "QUIT", ord('x'): "QUIT",
    ord('W'): "DEBUG", ord('w'): "DEBUG",
    ord('I'): "INVENTORY", ord('i'): "INVENTORY",
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
}
HUD_ACTIONS = {"INVENTORY", "QUIT", "DEBUG"}
HUD_KEYS = {}
for k, v in KEY_MAPPING.items():
    if v in HUD_ACTIONS and v not in HUD_KEYS.values():
        HUD_KEYS[k] = v

# chiffres 0-9 → renvoie directement l'entier
for i in range(10):
    KEY_MAPPING[ord(str(i))] = i


def key_to_action(key):
    return KEY_MAPPING.get(key, key)

# modes de "gameplay"

def exploration_mode(self, stdscr):
    self.show_scene(stdscr)
    self.draw_player(stdscr)
    self.draw_entities(stdscr)
    # self.draw_events(stdscr) # events dont have sprite for now
    self.draw_hud(stdscr)

def dialogue_mode(self, stdscr):
    if self.universe.dialogue_system.current_dialogue:
        self.universe.dialogue_system.current_say = self.get_dialogue_segment(((self.screens["hud"]["size"][0]-1)//2), self.screens["hud"]["size"][1]-2)
        self.draw_dialogue_lines(stdscr, "hud", 1, 1, self.universe.dialogue_system.current_say)
    if self.universe.dialogue_system.state == "CHOICE":
        self.draw_dialogue_lines(stdscr, "hud",1,1, self.universe.dialogue_system.current_say)

        for idx, choice in enumerate(self.universe.dialogue_system.choices):
            self.draw(stdscr, "hud", idx + self.screens["hud"]["size"][0]//2, 1, f"{idx + 1}. {choice}")
    sprite, (max_x, max_y) = self.load_sprite("assets/sprites/{}.txt".format(self.universe.dialogue_system.speaker))
    self.draw_sprite("scene",sprite, self.screens["scene"]["size"][0]-max_y-1, (self.screens["scene"]["size"][1]-max_x)//2, stdscr)

def inventory_mode(self, stdscr):
    self.draw(stdscr, "hud", 0, 0, "Inventory:")
    for idx, (item_name, quantity) in enumerate(self.universe.player.inventory.items()):
        item = get_item(item_name)
        self.draw(stdscr, "hud", idx + 2, 0, f"{item['name']} x{quantity}")

def combat_mode(self, stdscr):
    # TODO: changer la variable là qui se fait à chaque itération, ça sert à rien bordel
    self.draw(stdscr, "hud", 0, 0, "COMBAT MODE")
    nb_enemies = len(self.universe.combat_system.fighters)
    for idx, enemy in enumerate(self.universe.combat_system.fighters):
        enemy_sprite, (max_x, max_y) = self.load_sprite("assets/sprites/{}.txt".format(enemy.id))
        x = 1 + (idx + 1) * (self.universe.size[1] - 2) // (nb_enemies + 1) - max_x // 2
        y = (self.universe.size[0] - 1) // 2 - max_y - 2
        self.draw(stdscr, "scene", (self.universe.size[0] - 1) // 2 - 2, x, f"{enemy.name}")
        self.draw(stdscr, "scene", (self.universe.size[0] - 1) // 2 - 1, x, f"{enemy.hp}/{enemy.max_hp}")

        self.draw_sprite("scene",enemy_sprite, y, x, stdscr)

    self.draw(stdscr, "hud", 1, 1, "Player HP: {}".format(self.universe.player.hp))

    q0 = self.combat_system.queue[0] if self.combat_system.queue else ""

    if self.combat_system.state == "START":
        self.draw(stdscr, "hud", 1, 1, "A wild enemy appears!")
    elif self.combat_system.state == "PLAYER_TURN":
        if q0 == "PLAYER_CHOICE":
            self.draw(stdscr, "hud", 1 + 1, 1, "Choose your action:")
            self.draw_button(stdscr, "hud", 1 + 1 + 1, 1, "1. Attack")
            self.draw_button(stdscr, "hud", 1 + 2 + 2+1, 1, "2. Ability")
            self.draw_button(stdscr, "hud", 1 + 2 + 4+2, 1, "3. Use Item")
        elif q0 == "ABILITY_CHOICE":
            self.draw(stdscr, "hud", 1 + 1, 1, "Choose your ability:")
            self.draw(stdscr, "hud", 1 + 1 + 1, 1, "0. Back")
            for idx, ability in enumerate(self.universe.player.ext_data["abilities"].values()):
                self.draw(stdscr, "hud", 1 + 1 + 2 + idx, 1, f"{idx + 1}. {ability['name']}")
        elif q0 == "ITEM_CHOICE":
            self.draw(stdscr, "hud", 1 + 1, 1, "Choose your item:")
            self.draw(stdscr, "hud", 1 + 1 + 1, 1, "0. Back")
            inventory_items = list(self.universe.player.inventory.keys())
            for idx, item_name in enumerate(inventory_items):
                item_data = get_item(item_name)
                quantity = self.universe.player.inventory[item_name]
                if quantity > 0 and item_data["type"] == "consumable":
                    self.draw(stdscr, "hud", 1 + 2 + 1 + idx, 1, f"{idx + 1}. {item_data['name']} x{quantity}")
        elif q0 == "CHOOSE_TARGET":
            self.draw(stdscr, "hud", 1 + 1, 1, "Choose your target:")
            self.draw(stdscr, "hud", 1 + 1 + 1, 1, "0. Back")
            for idx, enemy in enumerate(self.combat_system.fighters):
                self.draw(stdscr, "hud", 1 + 2 + 1 + idx, 1, f"{idx + 1}. {enemy.name}")
        elif q0:
            self.draw(stdscr, "hud", 1 + 1, 1, q0)


    elif self.combat_system.state == "ENEMIES_TURN" and q0:
        self.draw(stdscr, "hud", 1 + 1, 1, q0)
    elif self.combat_system.state == "VICTORY":
        self.draw(stdscr, "hud", 1 + 1 + 2, 1, "You won the combat!")
        self.draw(stdscr, "hud", 1 + 1 + 3, 1, "Loot:")
        for idx, (item_id, quantity) in enumerate(self.combat_system.loot):
            item = get_item(item_id)
            self.draw(stdscr, "hud", 1 + 1 + 4 + idx, 1, f"{item['name']} x{quantity}")

def debug_mode(self, stdscr):
    exploration_mode(self, stdscr)
    self.draw(stdscr, "hud", 1, 1 + self.screens["hud"]["size"][1] - 12, "DEBUG MODE")

class CursesUI:
    def __init__(self, universe):
        self.universe = universe
        self.modes = {
            "exploration": exploration_mode,
            "dialogue": dialogue_mode,
            "inventory": inventory_mode,
            "debug": debug_mode,
            "combat": combat_mode
        }
        self.cursor = (0, 0)

        # the area for screen, the border is inculded
        self.screens = {
            "scene": {
                "position": (0, 0),
                "size": (universe.size[0] // 2, universe.size[1]),
            },
            "hud": {
                "position": (universe.size[0] - universe.size[0] // 2, 0),
                "size": (universe.size[0] // 2, universe.size[1]),
            }
        }


        if charged:
            self.modes.update(ui_ext.ui_modes)

        self.mode_draw_function = self.modes[universe.mode]
        self.universe.set_mode_change_callback(self.change_mode)

        self.combat_system = self.universe.combat_system

    def run(self):
        curses.wrapper(self.main_loop)

    def change_mode(self, mode):
        self.mode_draw_function = self.modes.get(mode, exploration_mode)

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)  # getch make things waiting | edit I have no idea wtf this means

        while True:
            stdscr.erase()

            if stdscr.getmaxyx()[0] <= self.universe.size[0] or stdscr.getmaxyx()[1] <= self.universe.size[1]:
                stdscr.addstr(0, 0, "Veuillez agrandir la fenêtre")

            else:
                self.mode_draw_function(self, stdscr)
                self.draw_border(self.screens["scene"]["position"],self.screens["scene"]["size"], stdscr)
                self.draw_border(self.screens["hud"]["position"],self.screens["hud"]["size"], stdscr)
                key = stdscr.getch()
                stdscr.addstr(10, 10, f"Mode: {key}")
                self.universe.input_system(self.universe, key_to_action(
                    key))  # traite l'entrée et la convertit en action que le système peut comprendre

            stdscr.refresh()



    def show_scene(self, stdscr):
        scene = self.universe.scenes[self.universe.current_world]
        for y, ligne in enumerate(scene.map_data):
            self.draw(stdscr, "scene", y, 0, ligne)

    def draw_player(self, stdscr):
        player = self.universe.player
        y, x = player.position
        self.draw(stdscr, "scene", y, x, player.sprite)

    def draw_entity(self, stdscr, entity):
        y, x = entity.position
        self.draw(stdscr, "scene", y, x, entity.sprite)

    def draw_entities(self, stdscr):
        scene = self.universe.scenes[self.universe.current_world]
        for entity in scene.entities.values():
            self.draw_entity(stdscr, entity)

    def draw_event(self, stdscr, event):
        y, x = event.position
        self.draw(stdscr, "scene", y, x, event.sprite)

    def draw_events(self, stdscr):
        scene = self.universe.scenes[self.universe.current_world]
        for event in scene.event_system.events.values():
            self.draw_event(stdscr, event)

    def draw_hud(self, stdscr):
        # draw hud at fixed coordinate like for exemple for now like this : [key] : action
        for idx, (k, v) in enumerate(HUD_KEYS.items()):
            self.draw(stdscr, "hud", idx + 0 + 1, 0 + 1, f"[{chr(k)}] : {v}")

    def draw_border(self, position, size, stdscr):
        """

        :param position: (y,x)
        :param size: (h,w)
        :param stdscr:
        :return:
        """
        h, w = size
        y, x = position

        # Bordures
        stdscr.addstr(y, x, '┌' + '─' * (w - 2) + '┐')
        stdscr.addstr(y + h - 1, x, '└' + '─' * (w - 2) + '┘')

        # Bordures latérales sans remplir
        for i in range(1, h - 1):
            stdscr.addstr(y + i, x, '│')
            stdscr.addstr(y + i, x + w - 1, '│')

    def convert_text_special(self, text):
        # unused for now
        """
        it checks if the character has to be turned into a special one
        :param stdscr:
        :param text:
        :param y:
        :param x:
        :return:
        """
        text_list = list(text)
        for idx, char in enumerate(text_list):
            if char in CHAR_MAP:
                text_list[idx] = CHAR_MAP[char]
        return ''.join(text_list)

    def load_sprite(self, path):
        """
        Charge un sprite ASCII depuis un fichier texte.
        Retourne :
            - liste des lignes
            - largeur maximale (max_x)
            - hauteur (max_y)
        """
        sprite_lines = []
        max_x = 0
        max_y = 0

        with open(path, "r") as f:
            for line in f:
                line = line.rstrip("\n")
                sprite_lines.append(line)

                length = len(line)
                if length > max_x:
                    max_x = length

                max_y += 1

        return sprite_lines, (max_x, max_y)

    def draw_sprite(self, scene, sprite_lines, y, x, stdscr):
        """
        Affiche un sprite ligne par ligne à partir d'une liste de lignes.
        sprite_lines = liste obtenue via load_sprite().
        """
        a,b = self.screens[scene]["position"]
        for idx, line in enumerate(sprite_lines):
            # Chaque ligne est dessinée à la position (y + idx, x)
            stdscr.addstr(y + idx+a, x+b, line)

    def draw(self, stdscr, scene, y, x, text):
        """
        Dessine du texte à une position relative à une scène (scene ou hud).
        Les positions de la scène sont ajoutées aux coordonnées fournies.
        :param scene:
        :param y:
        :param x:
        :param text:
        :param stdscr:
        :return:
        """
        if scene in self.screens:
            pos = self.screens[scene]["position"]
        else:
            pos = (0, 0)
        text = self.convert_text_special(text)
        stdscr.addstr(y + pos[0], x + pos[1], text)

    def draw_text(self, stdscr, scene, y, x, text):
        x_max = self.screens[scene]["size"][1] - 2 - x
        words = text.split()
        current_line = ""
        size_line = 0

        for word in words:
            size_word = len(word)
            space_needed = 1 if current_line else 0

            # Le mot tient dans la ligne courante
            if size_line + size_word + space_needed <= x_max:
                if current_line:
                    current_line += " "
                    size_line += 1
                current_line += word
                size_line += size_word

            else:
                # On affiche la ligne courante
                if current_line:
                    self.draw(stdscr, scene, y, x, current_line)
                    y += 1

                # Découper les mots trop longs
                while size_word > x_max:
                    part = word[:x_max - 1] + "-"  # Xmax-1 + "-" = Xmax
                    self.draw(stdscr, scene, y, x, part)
                    y += 1
                    word = word[x_max - 1:]
                    size_word = len(word)

                # Le reste du mot pour après
                current_line = word
                size_line = size_word

        # Dernière ligne
        if current_line:
            self.draw(stdscr, scene, y, x, current_line)

    def segment_text(self, stdscr, scene,y,x):
        max_text = ((self.screens[scene]["size"][0]-1)//2) * (self.screens[scene]["size"][1]-2)
        if len(self.universe.dialogue_system.current_dialogue)> max_text:
            while self.universe.dialogue_system.current_dialogue[max_text] !=" ":
                max_text -=1
            new_text = self.universe.dialogue_system.current_dialogue[:max_text]
            self.universe.dialogue_system.current_dialogue = \
                self.universe.dialogue_system.current_dialogue[max_text:]
            return new_text
        else:
            return self.universe.dialogue_system.current_dialogue

    def get_dialogue_segment(self, max_lines, x_max):
        """
        Extrait un segment du dialogue, mot par mot, jusqu'à max_lines et x_max par ligne.
        Retourne une liste de lignes à afficher et met à jour current_dialogue.
        """
        text = self.universe.dialogue_system.current_dialogue
        words = text.split()
        y_used = 0
        current_line = ""
        size_line = 0
        displayed_words = 0
        lines_to_draw = []

        for word in words:
            word_len = len(word)
            space_needed = 1 if current_line else 0

            if size_line + word_len + space_needed <= x_max:
                if current_line:
                    current_line += " "
                    size_line += 1
                current_line += word
                size_line += word_len
            else:
                # ligne complète
                lines_to_draw.append(current_line)
                y_used += 1
                if y_used >= max_lines:
                    break

                # découper les mots trop longs
                while word_len > x_max:
                    part = word[:x_max - 1] + "-"
                    lines_to_draw.append(part)
                    y_used += 1
                    if y_used >= max_lines:
                        break
                    word = word[x_max - 1:]
                    word_len = len(word)

                current_line = word
                size_line = len(word)

            displayed_words += 1

        if y_used < max_lines and current_line:
            lines_to_draw.append(current_line)

        # mise à jour du dialogue restant
        self.universe.dialogue_system.current_dialogue = " ".join(words[displayed_words:])
        if self.universe.dialogue_system.current_dialogue == "":
            self.universe.dialogue_system.notify_reading_consumed()

        return lines_to_draw

    def draw_dialogue_lines(self, stdscr, scene, y, x, lines):
        """Affiche les lignes déjà préparées."""
        for idx, line in enumerate(lines):
            self.draw(stdscr, scene, y + idx, x, line)

    def draw_button(self, stdscr, scene, y, x, text):
        """Dessine un bouton avec du texte centré."""
        (border_y,border_x) = y + self.screens[scene]["position"][0], x + self.screens[scene]["position"][1]
        button_width = len(text) + 4  # 2 espaces de chaque côté
        self.draw_border((border_y, border_x), (3, button_width), stdscr)
        self.draw(stdscr, scene, y + 1, x + 2, text)



