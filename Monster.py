from Character import *


class Monster(Character):
    def __init__(self, level):
        super(Monster, self).__init__("skeleton", level, "Monster")
        self.has_the_key = False
        # setting the initial stats of the monster
        self.stats.set_stats(
            2 * self.level * roll_dice(),
            self.level / 2 * roll_dice(),
            self.level * roll_dice(),
            True
        )

    def give_the_key(self):
        self.has_the_key = True