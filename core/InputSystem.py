class InputSystem:
    def __init__(self, univers):
        self.univers = univers


    def process_input(self, key):
        if key == "UP":
            self.univers.player.move(-1, 0)  # Déplacer vers le haut
        elif key == "DOWN":
            self.univers.player.move(1, 0)   # Déplacer vers le bas
        elif key == "LEFT":
            self.univers.player.move(0, -1)  # Déplacer vers la gauche
        elif key == "RIGHT":
            self.univers.player.move(0, 1)   # Déplacer vers la droite

