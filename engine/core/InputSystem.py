import os
from engine.core.logging_setup import logger
import world
import engine.core.ItemManager as ItemManager



if os.path.exists("extensions/input_extensions.py") and os.path.isfile("extensions/input_extensions.py"):
    import extensions.input_extensions as input_ext
    charged = True
else:
    logger.warning(f"Module 'extension/input_extensions' is missing. please run setup_environment.py. from engine")
    charged = False


def exploration_input(universe, key):
    if key == "UP":
        universe.player.move(-1, 0)  # Déplacer vers le haut
        universe.player.orientation = "UP"
    elif key == "DOWN":
        universe.player.move(1, 0)   # Déplacer vers le bas
        universe.player.orientation = "DOWN"
    elif key == "LEFT":
        universe.player.move(0, -1)  # Déplacer vers la gauche
        universe.player.orientation = "LEFT"
    elif key == "RIGHT":
        universe.player.move(0, 1)   # Déplacer vers la droite
        universe.player.orientation = "RIGHT"
    elif key in hud:
        universe.mode_change(key.lower())



    elif key == "INTERACT":
        ...

    universe.current_scene.event_system.update(universe.player, key)

def dialogue_input(universe, key):
    if universe.dialogue_system.state == "TEXT_CHUNK":
        if key == "INTERACT":
            ...
    elif universe.dialogue_system.state == "CHOICE":
        if isinstance(key, int):  # renvoie d'un chiffre via le mapping
            if 1 <= key <= len(universe.dialogue_system.choices):
                universe.dialogue_system.set_next_line(choice_index=key - 1)

    elif universe.dialogue_system.state == "NEXT_LINE":
        if key == "INTERACT":
            universe.dialogue_system.set_next_line()

def inventory_input(universe, key):
    if key == "INVENTORY":
        universe.mode_change("exploration")

def debug_input(universe, key):
    exploration_input(universe, key)  # garder les contrôles d'exploration

    if key == ord('b'):
        universe.mode_change("exploration")
        # TODO: remove debug keys
    if key == ord('r'):
        universe.set_scene(world.Test)
    elif key == ord('n'):
        universe.set_scene(world.Test2)
    elif key == ord('y'):
        universe.set_scene(world.Test3)
    elif key == ord('m'):
        universe.mode_change("dialogue")
    elif key == ord('p'):
        universe.mode_change("exploration")
    elif key == ord('o'):
        universe.player.add_to_inventory("health_potion", 10)
        universe.player.add_to_inventory("bomb", 5)
    elif key == ord('l'):
        universe.mode_change("inventory")
    elif key == 'TEST':
        universe.mode_change("exploration")
    elif key == ord('b'):
        universe.mode_change("combat")
        universe.combat_system.add_fighter("goblin")
        universe.combat_system.add_fighter("goblin")

def combat_input(universe, key):
    # Placeholder for combat input handling
    if universe.combat_system.state == "START":
        if key == "INTERACT":
            universe.combat_system.player_turn()
    elif universe.combat_system.state == "PLAYER_TURN":
        if universe.combat_system.queue:
            if universe.combat_system.queue[0] == "PLAYER_CHOICE":
                if isinstance(key, int):
                    if key == 1:
                        universe.combat_system.player_action["action"] = "attack"
                        universe.combat_system.queue.pop(0)
                        universe.combat_system.queue.insert(0, "CHOOSE_TARGET")
                    elif key == 2:
                        universe.combat_system.queue.append("ABILITY_CHOICE")
                        universe.combat_system.queue.pop(0)
                    elif key == 3:
                        universe.combat_system.queue.append("ITEM_CHOICE")
                        universe.combat_system.queue.pop(0)
            elif universe.combat_system.queue[0] == "ABILITY_CHOICE":
                if isinstance(key, int):
                    if key == 0:
                        universe.combat_system.queue.pop(0)
                        universe.combat_system.queue.insert(0, "PLAYER_CHOICE")
                        return
                    abilities = list(universe.player.ext_data["abilities"].values())
                    if 1 <= key <= len(abilities):
                        universe.combat_system.player_action["action"] = "ability"
                        universe.combat_system.player_action["data"] = abilities[key - 1]
                        universe.combat_system.queue.pop(0)
                        universe.combat_system.queue.insert(0, "CHOOSE_TARGET")
            elif universe.combat_system.queue[0] == "ITEM_CHOICE":
                if isinstance(key, int):
                    if key == 0:
                        universe.combat_system.queue.pop(0)
                        universe.combat_system.queue.insert(0, "PLAYER_CHOICE")
                        return
                    inventory_items = list(universe.player.inventory.keys())
                    if 1 <= key <= len(inventory_items):
                        if not universe.player.inventory[inventory_items[key - 1]]:
                            # If the item quantity is zero, ignore the choice
                            return
                        item_data = ItemManager.get_item(inventory_items[key - 1])
                        if item_data["type"] != "consumable":
                            # If the item is not usable in combat, ignore the choice
                            return
                        universe.combat_system.player_action["action"] = "use_item"
                        universe.combat_system.player_action["data"] = item_data
                        if "damage" in item_data["effect"]:
                            universe.combat_system.queue.pop(0)
                            universe.combat_system.queue.insert(0, "CHOOSE_TARGET")
                        else:
                            universe.combat_system.queue.pop(0)
                            universe.combat_system.execute_player_action()

            elif universe.combat_system.queue[0] == "CHOOSE_TARGET":
                if isinstance(key, int):
                    if key == 0:
                        universe.combat_system.queue.pop(0)
                        universe.combat_system.queue.insert(0, "PLAYER_CHOICE")
                        return
                    if 1 <= key <= len(universe.combat_system.fighters):
                        universe.combat_system.player_action["target"] = universe.combat_system.fighters[key - 1]
                        universe.combat_system.queue.pop(0)
                        universe.combat_system.execute_player_action()

            else:
                # In combat, any key press could advance the combat log
                universe.combat_system.queue.pop(0)
        if not universe.combat_system.queue:
            # If the queue is empty, proceed to the next round
            universe.combat_system.enemies_turn()
    elif universe.combat_system.state == "ENEMIES_TURN":
        # During enemies' turn, we can just wait for the turn to end
        if universe.combat_system.queue:
            # In combat, any key press could advance the combat log
            universe.combat_system.queue.pop(0)
        if not universe.combat_system.queue:
            universe.combat_system.new_round()
    elif universe.combat_system.state == "VICTORY":
        if key == "INTERACT":
            universe.combat_system.give_loot()
            universe.combat_system.reset_combat()
            universe.mode_change("exploration")



modes = {
    "exploration": exploration_input,
    "dialogue": dialogue_input,
    "inventory": inventory_input,
    "debug": debug_input,
    "combat": combat_input,
}

# hud is the input handler for the hud elements like inventory and things like that, to add more if needed
hud = {"INVENTORY", "DEBUG"}

if charged:
    modes.update(input_ext.input_modes)

