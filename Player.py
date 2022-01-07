class Player(object):
    def __init__(self, name, color, first):
        self.name = name
        self.color = color
        self.first = first

    def __str__(self):
        return f"Player: {self.name}, {self.color}"
