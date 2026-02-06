import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random
import sys, os
import struct, threading, socket
import json, glob


class GameSnake:
    
    VELOCITY_MAP = {"Up": [0, -1], "Down": [0, 1], "Left": [-1, 0], "Right": [1, 0]}
    TILE_MAP = {'snake': 'green', 'food': 'red'}

    def __init__(self, tile_cnt, tile_size, host='127.0.0.1', port=49152):
        self.host = host
        self.port = port
        self.socket = None
        
        self.tile_cnt = tile_cnt
        self.tile_size = tile_size    
        self.direction = ["Up", "Up"]
        self.velocity = GameSnake.VELOCITY_MAP[self.direction[0]]
        self.root = tk.Tk()
        self.root.title("Snake")
        self.root.geometry("%dx%d" % (self.tile_cnt * self.tile_size, self.tile_cnt * self.tile_size))
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=self.tile_cnt * self.tile_size, height=self.tile_cnt * self.tile_size,
                                bg="lightgray")
        self.canvas.pack()
        # TODO: 260114 Done. menu with save, load, reset
        frame_menu = tk.Frame(self.root)
        self.frame_menu_id = self.canvas.create_window((self.tile_cnt * self.tile_size / 2, self.tile_cnt * self.tile_size / 2), width = self.tile_size * 4, window=frame_menu, anchor=tk.CENTER)
        self.canvas.itemconfig(self.frame_menu_id, state=tk.HIDDEN)  
        button_save = tk.Button(frame_menu, text='Save', command=self.on_btnsave)
        button_save.pack(fill='x', expand=True)
        button_load = tk.Button(frame_menu, text='Load', command=self.on_btnload)
        button_load.pack(fill='x', expand=True)
        button_reset = tk.Button(frame_menu, text='Reset', command=self.on_btnreset)
        button_reset.pack(fill='x', expand=True)
        
        self.root.bind('<Key>', self.on_keypress)
        self.snake_head = self.Tile('snake', self, 5, 5)
        self.snake_body = []
        self.snake_body.append(self.snake_head)
        self.food = self.Tile('food', self)

        self.paused = False
        self.game_over = False

    class Tile:
        def __init__(self, type, game, x=None, y=None):
            self.type = type
            self.id = None
            # TODO: 260115 Done. Food does not init on snake_body
            if x is None or y is None:
                self.x, self.y = random.randint(0, game.tile_cnt - 1), random.randint(0, game.tile_cnt - 1)
                while GameSnake.collide_list(self, game.snake_body):
                    self.x, self.y = random.randint(0, game.tile_cnt - 1), random.randint(0, game.tile_cnt - 1)
            else:
                self.x, self.y = x, y
            game.draw_tile(self)

        def to_dict(self):
            return {
                'type': self.type,
                'x': self.x,
                'y': self.y
                }

    def on_btnsave(self):
        print('on_btnsave')
        # game_state as direction, snake_body, food. maybe tile_cnt, tile_size later
        game_state = {'direction':self.direction, 'tile':[snake_part.to_dict() for snake_part in self.snake_body] + [self.food.to_dict()]}
        datestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f")
        with open(f'./save/%s.json' %datestamp, 'w') as f:
            json.dump(game_state, f, indent=4)

    def on_btnload(self):
        print('on_btnload')
        self.clear()
        file_latest = max(glob.glob('./save/*.json'), key=os.path.getctime)
        with open(file_latest, 'r') as f:
            game_state = json.load(f)
        self.direction = game_state.get('direction')
        for tile in game_state.get('tile'):
            tile_obj = self.Tile(tile.get('type'), self, tile.get('x'), tile.get('y'))
            if tile_obj.type == 'snake':
                self.snake_body.append(tile_obj)
            elif tile_obj.type == 'food':
                self.food = tile_obj
        self.snake_head = self.snake_body[0]
        if self.game_over:
            self.game_over = False
            self.move()

    def on_btnreset(self):
        print('on_btnreset')
        # delete snake_body, food
        self.clear()
        self.snake_head = self.Tile('snake', self, 5, 5)
        self.snake_body.append(self.snake_head)
        self.food = self.Tile('food', self)
        if self.game_over:
            self.game_over = False
            self.move()

    def clear(self):
        for snake_part in self.snake_body:
            self.canvas.delete(snake_part.id)
        self.canvas.delete(self.food.id)
        self.snake_body.clear()
    
    def move(self):
        if self.paused:
            self.root.after(400, self.move)
            return
        elif self.game_over:
            print("game over")
            return
        print('move')
        print('direction', self.direction)
        if GameSnake.collide(self.snake_head, self.food):
            self.food.type = 'snake'
            self.snake_body.append(self.food)  # food into part of snake_body, color to green
            self.food = self.Tile('food', self)
        self.direction[0] = self.direction[1]
        self.velocity = GameSnake.VELOCITY_MAP[self.direction[0]]
        print('velocity', self.velocity)
        temp_x = self.snake_head.x + self.velocity[0]
        temp_y = self.snake_head.y + self.velocity[1]
        for i, snake_part in enumerate(self.snake_body):
            #print("%d index in snake_body x: %d y: %d before" % (i, snake_part.x, snake_part.y))
            snake_part.x, temp_x = temp_x, snake_part.x
            snake_part.y, temp_y = temp_y, snake_part.y
            self.draw_tile(snake_part)
            #print("%d index in snake_body x: %d y: %d after" % (i, snake_part.x, snake_part.y))
        self.check_end()
        self.root.after(400, self.move)

    def check_end(self):
        if self.snake_head.x < 0 or self.snake_head.x > self.tile_cnt - 1 or self.snake_head.y < 0 or self.snake_head.y > self.tile_cnt - 1:
            self.game_over = True
        self.game_over = GameSnake.collide_list(self.snake_head, self.snake_body[1:])

    def draw_grid(self):
        for i in range(self.tile_cnt):
            self.canvas.create_line(0 * self.tile_size, i * self.tile_size, self.tile_cnt * self.tile_size,
                                    i * self.tile_size, fill='gray', tags='grid_line')
            self.canvas.create_line(i * self.tile_size, 0 * self.tile_size, i * self.tile_size,
                                    self.tile_cnt * self.tile_size, fill='gray', tags='grid_line')
        #TODO: 260114 Done. Initial snake_part and food created in init() before run() calls draw_grid. need to move grid_line to below those tiles
        self.canvas.lower('grid_line')

    def draw_tile(self, tile):
        x1, y1 = tile.x * self.tile_size, tile.y * self.tile_size
        x2, y2 = x1 + self.tile_size, y1 + self.tile_size
        if tile.id:           
            self.canvas.coords(tile.id, x1, y1, x2, y2)
            self.canvas.itemconfig(tile.id, fill=GameSnake.TILE_MAP.get(tile.type))
        else:
            tile.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=GameSnake.TILE_MAP.get(tile.type))

    def on_keypress(self, event):
        # TODO: Done, only 1 update per game loop, use direction[0] and direction[1]
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
        elif key_sym == "p" or key_sym == "P":
            self.paused = not self.paused
            self.canvas.itemconfig(self.frame_menu_id, state=(tk.NORMAL if self.paused else tk.HIDDEN))

    @staticmethod
    def collide(tile1, tile2):
        return tile1.x == tile2.x and tile1.y == tile2.y

    @staticmethod
    def collide_list(tile, tile_list):
        for i, tile_part in enumerate(tile_list):
            if GameSnake.collide(tile, tile_part):
                print("%d index in tile_list x: %d y: %d collide with tile x: %d y: %d" % (i, tile_part.x, tile_part.y, tile.x, tile.y))
                return True
        return False

    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            s.settimeout(1)
            print('connected\n', s)
            self.socket = s
    
    def run(self):
        threading.Thread(target=self.run_listener).start()
        self.draw_grid()
        self.move()
        print("root.after completed")
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        game_snake = GameSnake(20, 25)
    elif sys.argv[1].isdigit() and sys.argv[2].isdigit():
        # disable variable size and scale due to save and load
        game_snake = GameSnake(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("usage: game_snake.py <tile_count> <tile_size>")
        sys.exit()
    game_snake.run()
