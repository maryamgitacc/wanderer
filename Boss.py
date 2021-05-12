from Character import *


class Boss(Character):
    def __init__(self, level):
        super(Boss, self).__init__("boss", level, "Boss")
        # setting the initial stats of the monster
        self.stats.set_stats(
            (2 * self.level * roll_dice()) + roll_dice(),
            (self.level / 2 * roll_dice()) + (roll_dice() / 2),
            (self.level * roll_dice()) + self.level,
            True
        )