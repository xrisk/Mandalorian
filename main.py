import sys
import numpy as np
from time import sleep

from screen import Screen
from mando import Mando
from entity import Entity
from floor import Floor, Sky
from coin import Coin
from collections import defaultdict
from beam import Beam
from magnet import Magnet
from dragon import Dragon

import threading
import colorama

import time
import os

from random import randint, choice

last_char = b""
lock = threading.Lock()


def getchar():
    # w -> up
    # a -> left
    # d -> right
    # q -> shoot
    # b -> boost
    # <space> -> shield
    whitelist = b"wadqb "
    global last_char
    last = None
    fd = sys.stdin.fileno()
    while True:
        # sleep(0.1)
        char = os.read(fd, 1)
        if char and char in whitelist:
            with lock:
                last_char = char
                last = time.time()
        elif not last or time.time() - last > 0.25:
            with lock:
                last_char = b""


class Game:
    def __init__(self, row=38, col=500):
        self.__is_running = True
        self.__screen = Screen(row, col)
        self.__row = row
        self.__col = col
        self.__buf = np.zeros(shape=(row, col), dtype=object)
        self.__scene = []
        self.__ticks = 0
        self.__input = b""
        self._backing = defaultdict(list)
        self.__score = 0
        self.__total_time = 120
        self.__last_shield_time = None
        self.__shield_cooldown = 60
        self.__fps = 30
        self.__actual_fps = 0

    def process_input(self):
        with lock:
            tmp = last_char
        self.__input = tmp

    def add_entity(self, e):
        self.__scene.append(e)

    def increment_score(self, d):
        self.__score += d

    def tick(self):
        self.__ticks += 1
        self.__buf.fill(" ")
        self._backing.clear()
        for entity in self.__scene:
            entity.tick(self.__buf)
            entity.render(self.__buf)

    def draw(self, l, r, banner):
        self.__screen.render(self.__buf, l, r, banner)

    def get_rows(self):
        return self.__row

    def get_cols(self):
        return self.__col

    def generate_coins(self):
        n_coin = 200
        for _ in range(n_coin):
            while True:
                r = randint(4, self.__row - 6)
                c = randint(0, self.__col - 1)
                if not self._backing[(r, c)]:
                    break
            self.add_entity(Coin(r, c, self))

    def generate_beams(self):
        for _ in range(30):
            r = randint(4, self.__row - 10)
            c = randint(50, self.__col - 10)
            t = Beam(r, c, g)
            t.set_orientation(choice(["vert", "horiz", "diag"]))
            t.render(self.__buf)
            self.add_entity(t)

    def init_scene(self):
        self.add_entity(Sky(0, 0, g))
        self.add_entity(Floor(0, 0, g))
        self.generate_beams()
        self.generate_coins()
        self.add_entity(Magnet(5, 50, g))
        self.add_entity(Dragon(10, 450, g))

        self.__mando = Mando(10, 0, g)
        self.add_entity(self.__mando)

    def get_mando(self):
        return self.__mando

    def append_backing(self, r, c, val):
        self._backing[(r, c)].append(val)

    def get_time_left(self):
        t = time.time() - self.__game_start_time
        assert t >= 0
        return int(self.__total_time - t)

    def get_shield_cooldown(self):
        if not self.__last_shield_time:
            return 0
        t = round(time.time() - self.__last_shield_time)
        return max(0, self.__shield_cooldown - t)

    def generate_banner(self):
        t = max(0, self.get_time_left())
        # assert t <= 120
        banner = f"Score: {self.__score} | Lives: {self.__mando.get_lives()} | Time Left: {t} | Shield Cooldown: {self.get_shield_cooldown()} | FPS: {self.__fps} | Actual FPS: {self.__actual_fps} |"
        return banner

    def stop_running(self):
        self.__is_running = False

    def should_terminate(self):
        return self.get_time_left() <= 0 or not self.__is_running

    def get_left_col(self):
        return self.__l

    def get_right_col(self):
        return self.__r

    def do_win(self):
        self.__end_message = "You win!"
        self.stop_running()

    def get_input(self):
        return self.__input

    def get_last_shield_time(self):
        return self.__last_shield_time

    def set_last_shield_time(self, val):
        self.__last_shield_time = val

    def set_fps(self, val):
        self.__fps = val

    def run(self):
        self.__l = 0
        self.__r = self.__l + 120
        self.__game_start_time = time.time()
        frame_ctr = 0
        try:
            self.__screen.initialize()
            self.init_scene()
            last = time.time()
            while not self.should_terminate():
                # print(self.l, self.mando.lives, self.input)
                self.process_input()
                self.tick()
                # print("here")
                self.draw(self.__l, self.__r, self.generate_banner())
                if self.__ticks % 5 == 0:
                    self.__l = min(self.__l + 1, self.__col - 120)
                    self.__r = min(self.__r + 1, self.__col)
                sleep(1 / self.__fps)
                t = time.time()
                self.__actual_fps = round(1 / (t - last))
                last = t
                print(self.get_shield_cooldown())
        except KeyboardInterrupt as ex:
            print(ex)
        finally:
            self.__screen.restore()
            os.system("clear")
            if self.__end_message:
                print(self.__end_message)
            else:
                print("Game Over!")


if __name__ == "__main__":
    threading.Thread(target=getchar, daemon=True).start()
    colorama.init()
    g = Game()
    g.run()
