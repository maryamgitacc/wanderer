class CharacterStats:
    def __init__(self, character):
        self.character = character
        self.max_health_point = 0
        self.health_point = 0
        self.defend_point = 0
        self.strike_point = 0

    def set_stats(self, mhp, dp, sp, reset_hp=False):
        self.max_health_point = mhp
        self.defend_point = dp
        self.strike_point = sp
        if reset_hp:
            self.health_point = mhp

    def __str__(self):
        return "HP: {0}/{1} | DP: {2} | SP: {3}".format(
            self.health_point,
            self.max_health_point,
            self.defend_point,
            self.strike_point
        )