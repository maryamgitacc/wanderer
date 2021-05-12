import random
from CharacterStats import CharacterStats


def roll_dice(sides=6):
    return random.randint(1, sides)


class Character:
    def __init__(self, img, level, name):
        self.x = 0
        self.y = 0
        self.img = img
        self.stats = CharacterStats(self)
        self.level = level
        self.name = name

    def move(self, x=0, y=0):
        self.x += x
        self.y += y

    def place(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_tile(self):
        return self.x, self.y

    def lose_health(self, points):
        self.stats.health_point -= points
        if self.stats.health_point < 0:
            self.stats.health_point = 0

    def gain_health(self, points):
        self.stats.health_point += points
        if self.stats.health_point > self.stats.max_health_point:
            self.stats.health_point = self.stats.max_health_point

    def is_alive(self):
        return self.stats.health_point > 0

    def __str__(self):
        if self.is_alive():
            return "{0} (Level {1}) {2}".format(
                self.name,
                self.level,
                self.stats
            )
        else:
            return "{0} (Level {1}) Dead".format(self.name, self.level)