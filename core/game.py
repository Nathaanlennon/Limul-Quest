class Game:
    def __init__(self):
        self.position = 0

    def move_right(self):
        self.position += 1

    def move_left(self):
        self.position -= 1

g = Game()
g.move_right()
print(g.position)
