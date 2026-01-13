import tkinter as tk
from tkinter import ttk
import random
import sys


class GameSnake:
    def __init__(self, tile_cnt, tile_size):
        self.tile_cnt = tile_cnt
        self.tile_size = tile_size
        self.velocity_map = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}
        self.direction = ["Up", "Up"]
        self.velocity = self.velocity_map[self.direction[0]]
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.geometry("%dx%d" % (self.tile_cnt * self.tile_size, self.tile_cnt * self.tile_size))
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=self.tile_cnt * self.tile_size, height=self.tile_cnt * self.tile_size,
                                bg="black")
        self.canvas.pack()
        self.root.bind('<Key>', self.on_keypress)
        self.snake_head = self.Tile("green", self, 5, 5)
        self.snake_body = []
        self.snake_body.append(self.snake_head)
        self.food = self.Tile("red", self)
        self.paused = False
        self.game_over = False

    class Tile:
        def __init__(self, color, game, x=None, y=None):
            self.color = color
            self.id = None
            self.x = x if x else random.randint(0, game.tile_cnt - 1)
            self.y = y if y else random.randint(0, game.tile_cnt - 1)
            game.draw_tile(self)

    def move(self):
        if self.paused:
            self.root.after(400, self.move)
            return
        elif self.game_over:
            print("game over")
            return
        print("move")
        if GameSnake.collide(self.snake_head, self.food):
            self.food.color = "green"
            self.snake_body.append(self.food)  # food into part of snake_body, color to green
            self.food = self.Tile("red", self)
        print("snake_body length: %d" % len(self.snake_body))
        self.direction[0] = self.direction[1]
        self.velocity = self.velocity_map[self.direction[0]]
        temp_x = self.snake_head.x + self.velocity[0]
        temp_y = self.snake_head.y + self.velocity[1]
        for snake_part in self.snake_body:
            snake_part.x, temp_x = temp_x, snake_part.x
            snake_part.y, temp_y = temp_y, snake_part.y
            self.draw_tile(snake_part)
        self.check_end()
        self.root.after(400, self.move)

    def check_end(self):
        if self.snake_head.x < 0 or self.snake_head.x > self.tile_cnt - 1 or self.snake_head.y < 0 or self.snake_head.y > self.tile_cnt - 1:
            self.game_over = True
        for snake_part in self.snake_body[1:]:
            if GameSnake.collide(self.snake_head, snake_part):
                self.game_over = True

    def draw_grid(self):
        for i in range(self.tile_cnt):
            self.canvas.create_line(0 * self.tile_size, i * self.tile_size, self.tile_cnt * self.tile_size,
                                    i * self.tile_size, fill="gray")
            self.canvas.create_line(i * self.tile_size, 0 * self.tile_size, i * self.tile_size,
                                    self.tile_cnt * self.tile_size, fill="gray")

    def draw_tile(self, tile):
        x1, y1 = tile.x * self.tile_size, tile.y * self.tile_size
        x2, y2 = x1 + self.tile_size, y1 + self.tile_size
        if tile.id:
            self.canvas.coords(tile.id, x1, y1, x2, y2)
            self.canvas.itemconfig(tile.id, fill=tile.color)
        else:
            tile.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=tile.color)
        # print("id: %s \t x: %d \t y: %d \t color: %s" % (tile.id, tile.x, tile.y, tile.color))

    def on_keypress(self, event):
        # need to allow only 1 update per game loop
        key_sym = event.keysym
        print(key_sym)
        if key_sym == "Up" and self.direction[0] != "Down":
            self.direction[1] = "Up"
        elif key_sym == "Down" and self.direction[0] != "Up":
            self.direction[1] = "Down"
        elif key_sym == "Left" and self.direction[0] != "Right":
            self.direction[1] = "Left"
        elif key_sym == "Right" and self.direction[0] != "Left":
            self.direction[1] = "Right"
        elif key_sym == "p":
            self.paused = not self.paused
        else:
            None

    @staticmethod
    def collide(tile1, tile2):
        return tile1.x == tile2.x and tile1.y == tile2.y

    def start(self):
        self.draw_grid()
        self.move()
        print("root.after completed")
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        game_snake = GameSnake(20, 25)
    elif sys.argv[1].isdigit() and sys.argv[2].isdigit():
        game_snake = GameSnake(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("usage: game_snake.py <tile_count> <tile_size>")
        sys.exit()
    game_snake.start()
