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

    elif key == "INTERACT":
        ...

    universe.current_scene.event_system.update(universe.player, key)

def dialogue_input(universe, key):
    if universe.dialogue_system.state == "TEXT_CHUNK":
        if key == "INTERACT":
            universe.dialogue_system.set_text_chunk()
    elif universe.dialogue_system.state == "CHOICE":
        if isinstance(key, int):  # renvoie d'un chiffre via le mapping
            if 1 <= key <= len(universe.dialogue_system.choices):
                universe.dialogue_system.set_next_line(choice_index=key - 1)
    elif universe.dialogue_system.state == "NEXT_LINE":
        if key == "INTERACT":
            universe.dialogue_system.set_next_line()




