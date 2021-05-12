from Hero import Hero
from Map import Map
from tkinter import *
from tkinter import messagebox
from Monster import Monster
from Character import *
from Boss import Boss


def generate_monster_level(area_level):
    rolled_dice = roll_dice(10)
    return area_level if 1 <= rolled_dice <= 5 else (area_level + 1 if rolled_dice <= 9 else area_level + 2)


class Game:
    def __init__(self, map_root):
        self.level = 1
        self.map = Map(map_root, self)
        self.hero = Hero(1)
        # placing the hero at the top-left corner
        self.hero.place()

        self.monsters = []
        self.boss = None
        # this property will hold a reference to the monster that is in the same place as the hero
        self.monster_in_tile = None
        self.create_monsters()

        map_root.bind('<Left>', self.left_key)
        map_root.bind('<Right>', self.right_key)
        map_root.bind('<Up>', self.up_key)
        map_root.bind('<Down>', self.down_key)
        map_root.bind('<space>', self.battle)

        # this holds a character object. comes handy when determining the attacker
        self.last_moved = None
        # keep track of the hero's moves, so we move the monsters after every 2 moves of the hero
        self.hero_moves_counter = 0

    def create_monsters(self):
        monster_count = 3 + roll_dice(3) - 1
        # determining monster levels(by predefined chances), creating monsters
        for _ in range(monster_count):
            self.monsters.append(Monster(generate_monster_level(self.level)))
        # and for the boss
        self.boss = Boss(generate_monster_level(self.level))
        # let's add the boss to the monsters list, just for simplicity
        self.monsters.append(self.boss)

        # finding random floors for placing the monsters
        placed_floors = []
        # this process includes the boss too, hence monster_count+1
        while len(placed_floors) < monster_count + 1:
            # 63 is the number of empty floors on the map
            rolled_dice = roll_dice(63)
            if rolled_dice == 1:
                continue
            if rolled_dice not in placed_floors:
                # placing the monster at floor
                x, y = self.map.get_nth_floor(rolled_dice)
                self.monsters[len(placed_floors) - 1].place(x, y)
                placed_floors.append(rolled_dice)

        # giving the key to the next area, to one of the 3 monsters
        key_holder = roll_dice(monster_count) - 1
        self.monsters[key_holder].give_the_key()

    # Binding keyboard key events to functions
    def left_key(self, event):
        if self.map.pos_is_free(self.hero.x - 1, self.hero.y):
            self.hero.move(x=-1)
            self.last_moved = self.hero
            self.hero_moves_counter += 1
            self.do_game_logic()
        self.hero.img = "hero_left"

    def right_key(self, event):
        if self.map.pos_is_free(self.hero.x + 1, self.hero.y):
            self.hero.move(x=1)
            self.last_moved = self.hero
            self.hero_moves_counter += 1
            self.do_game_logic()
        self.hero.img = "hero_right"

    def up_key(self, event):
        if self.map.pos_is_free(self.hero.x, self.hero.y - 1):
            self.hero.move(y=-1)
            self.last_moved = self.hero
            self.hero_moves_counter += 1
            self.do_game_logic()
        self.hero.img = "hero_up"

    def down_key(self, event):
        if self.map.pos_is_free(self.hero.x, self.hero.y + 1):
            self.hero.move(y=1)
            self.last_moved = self.hero
            self.hero_moves_counter += 1
            self.do_game_logic()
        self.hero.img = "hero_down"

    def check_hero_tile(self):
        any_monster = [monster for monster in self.monsters if monster.get_tile() == self.hero.get_tile()]
        if len(any_monster) == 1:
            self.monster_in_tile = any_monster[0]
        else:
            self.monster_in_tile = None

    def strike(self, attacker: Character, defender: Character):
        sv = attacker.stats.strike_point + (roll_dice() * 2)
        if sv > defender.stats.defend_point:
            defender.lose_health(sv - defender.stats.defend_point)

    def someone_died(self, character):
        if character is self.hero:
            # game over
            messagebox.showinfo("Game Over", "You lost.")
            self.map.master.destroy()
        else:
            self.monsters.remove(character)
            # level up hero
            self.hero.level_up()
            self.check_monsters_status()
        self.check_hero_tile()

    # performs a battle until one dies, then notifies the result to game.someone_died(character)
    def battle(self, event=None):
        if self.monster_in_tile is not None:
            # determining the attacker and the defender; who did the last move? (entered the tile)
            attacker = self.hero if self.last_moved is self.hero else self.monster_in_tile
            defender = self.monster_in_tile if attacker is self.hero else self.hero
            original_attacker = attacker

            who_died = None
            while attacker.is_alive() and defender.is_alive():
                self.strike(attacker, defender)
                if not (attacker.is_alive() and defender.is_alive()):
                    who_died = attacker if not attacker.is_alive() else defender
                    break
                else:
                    # switching the attacker and the defender, the defender strikes next
                    switching_temp = attacker
                    attacker = defender
                    defender = switching_temp
            self.someone_died(who_died)
            self.map.notify_battle(original_attacker, who_died)

    # this method is called after every character moves
    def do_game_logic(self):
        # checking if the hero is on a monster's tile
        self.check_hero_tile()

        # if a monster entered the hero's tile, a battle should be triggered
        if self.monster_in_tile is not None and self.last_moved is not self.hero:
            self.battle()

        # moving monsters after every 2 moves of the hero
        if self.last_moved is self.hero and self.hero_moves_counter == 2:
            self.hero_moves_counter = 0
            self.move_monsters()

    def check_monsters_status(self):
        monsters = self.monsters.copy()
        if self.boss.is_alive():
            # boss never carries the key
            monsters.remove(self.boss)

        hero_has_key = sum(monster.has_the_key for monster in monsters) == 0
        if hero_has_key and not self.boss.is_alive():
            self.enter_next_area()

    def move_monsters(self):
        for monster in self.monsters:
            current_tile = monster.get_tile()
            while True:
                random_direction = roll_dice(4)
                if random_direction == 1 and self.map.pos_is_free(current_tile[0], current_tile[1]-1):
                    monster.move(y=-1)
                    break
                elif random_direction == 2 and self.map.pos_is_free(current_tile[0]+1, current_tile[1]):
                    monster.move(x=+1)
                    break
                elif random_direction == 3 and self.map.pos_is_free(current_tile[0], current_tile[1]+1):
                    monster.move(y=+1)
                    break
                elif random_direction == 4 and self.map.pos_is_free(current_tile[0]-1, current_tile[1]):
                    monster.move(x=-1)
                    break
        self.last_moved = self.monsters
        self.do_game_logic()

    def enter_next_area(self):
        # hero restores some health upon entering next area
        hp_restore_dice = roll_dice(10)
        if hp_restore_dice == 1:
            # restore all hp
            self.hero.gain_health(self.hero.stats.max_health_point)
        elif 2 <= hp_restore_dice <= 5:
            # restore third of hp
            self.hero.gain_health(int(self.hero.stats.max_health_point / 3))
        else:
            # restore 10 percent of hp
            self.hero.gain_health(int(self.hero.stats.max_health_point / 10))

        self.monsters.clear()
        self.level += 1
        self.last_moved = None
        self.hero_moves_counter = 0
        self.monster_in_tile = None

        # creating new monsters
        self.create_monsters()
        self.hero.place(0, 0)

    def start(self):
        # this is the game loop
        # constantly running
        while True:
            self.map.update_screen()
