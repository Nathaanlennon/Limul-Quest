class InputSystem:
    def __init__(self, univers):
        self.univers = univers
        self.player = univers.player


    def process_input(self, key):
        if key == "UP":
            self.player.move(-1, 0)  # Déplacer vers le haut
            self.player.orientation = "UP"
        elif key == "DOWN":
            self.player.move(1, 0)   # Déplacer vers le bas
            self.player.orientation = "DOWN"
        elif key == "LEFT":
            self.player.move(0, -1)  # Déplacer vers la gauche
            self.player.orientation = "LEFT"
        elif key == "RIGHT":
            self.player.move(0, 1)   # Déplacer vers la droite
            self.player.orientation = "RIGHT"

        elif key == "INTERACT":
            ...

        self.univers.current_scene.event_system.update(self.univers.player, key)


