from tkinter import *


class Map:
    def __init__(self, master, game):
        self.game = game
        self.master = master
        master.title("The Wanderer")

        self.IMG_SIZE = 60
        self.WIDTH = 10 * self.IMG_SIZE
        self.HEIGHT = 10 * self.IMG_SIZE

        self.canvas = Canvas(master, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()

        directory = "images/"
        self.floor = PhotoImage(file=directory + "floor.png")
        self.wall = PhotoImage(file=directory + "wall.png")
        self.hero_down = PhotoImage(file=directory + "hero-down.png")
        self.hero_up = PhotoImage(file=directory + "hero-up.png")
        self.hero_right = PhotoImage(file=directory + "hero-right.png")
        self.hero_left = PhotoImage(file=directory + "hero-left.png")
        self.skeleton = PhotoImage(file=directory + "skeleton.png")
        self.boss = PhotoImage(file=directory + "boss.png")

        # [0][0] is the top left corner
        # zeros represent floors and ones are walls
        self.wall_map = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 0, 0, 0]
        ]

        self.hero_stats_label = Label(master)
        self.hero_stats_label.config(font=("Courier", 15))
        self.hero_stats_label.pack()

        self.monster_stats_label = Label(master)
        self.monster_stats_label.config(font=("Courier", 15))
        self.monster_stats_label.pack()

        self.battle_label = Label(master)
        self.battle_label.config(font=("Courier", 15))
        self.battle_label.pack()

    def get_pos_x(self, x):
        return self.IMG_SIZE * x

    def get_pos_y(self, y):
        return self.IMG_SIZE * y

    def pos_is_free(self, x, y):
        return (0 <= x <= 9 and 0 <= y <= 9) and (not self.wall_map[y][x])

    def get_nth_floor(self, n):
        k = 0
        for i in range(0, 10):
            for j in range(0, 10):
                if self.wall_map[i][j] == 0:
                    k += 1
                    if k == n:
                        # final coordinates of the empty random floor
                        return j, i
        return 0, 0

    def draw_map(self):
        for y, row in enumerate(self.wall_map):
            for x, tile in enumerate(row):
                # if tile == 1 : tile is True : tile is a wall
                if tile:
                    self.canvas.create_image(self.get_pos_x(x), self.get_pos_y(y), image=self.wall, anchor=NW)
                else:
                    self.canvas.create_image(self.get_pos_x(x), self.get_pos_y(y), image=self.floor, anchor=NW)

    # this method draws a character on the window canvas, regardless of its type(hero or monster)
    def draw_character(self, character):
        self.canvas.create_image(character.x * self.IMG_SIZE, character.y * self.IMG_SIZE,
                                 image=getattr(self, character.img), anchor=NW)

    def notify_battle(self, attacker, loser):
        self.battle_label.config(text="{0} attacked. {1} died.".format(attacker.name, loser.name))

    def update_screen(self):
        self.canvas.delete("all")
        self.draw_map()
        self.draw_character(self.game.hero)
        for monster in self.game.monsters:
            self.draw_character(monster)

        # updating character stats on the labels
        self.hero_stats_label.config(text=self.game.hero)
        if self.game.monster_in_tile is not None:
            self.monster_stats_label.config(text=self.game.monster_in_tile)
        else:
            self.monster_stats_label.config(text="")
        self.master.update_idletasks()
        self.master.update()
