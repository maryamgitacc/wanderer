from Character import *


class Hero(Character):
    def __init__(self, level):
        super(Hero, self).__init__("hero_down", level, "Hero")
        # setting the initial stats of the hero
        self.stats.set_stats(
            20 + (3 * roll_dice()),
            2 * roll_dice(),
            5 + roll_dice(),
            True
        )

    def level_up(self):
        self.level += 1
        self.stats.max_health_point += roll_dice()
        self.stats.strike_point += roll_dice()
        self.stats.defend_point += roll_dice()