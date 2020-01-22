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
    whitelist = b"wadq"
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
        self.is_running = True
        self.screen = Screen(row, col)
        self.row = row
        self.col = col
        self.buf = np.zeros(shape=(row, col), dtype=object)
        self.scene = []
        self.ticks = 0
        self.input = b""
        self.backing = defaultdict(list)
        self.score = 0
        self.total_time = 120

    def process_input(self):
        with lock:
            tmp = last_char
        self.input = tmp

    def add_entity(self, e):
        self.scene.append(e)

    def increment_score(self, d):
        self.score += d

    def tick(self):
        self.ticks += 1
        self.buf.fill(" ")
        self.backing.clear()
        for entity in self.scene:
            entity.tick(self.buf)
            entity.render(self.buf)

    def draw(self, l, r, banner):
        self.screen.render(self.buf, l, r, banner)

    def generate_coins(self):
        n_coin = 200
        for _ in range(n_coin):
            while True:
                r = randint(4, self.row - 6)
                c = randint(0, self.col - 1)
                if not self.backing[(r, c)]:
                    break
            self.add_entity(Coin(r, c, self))

    def generate_beams(self):
        for _ in range(30):
            r = randint(4, self.row - 10)
            c = randint(50, self.col - 10)
            t = Beam(r, c, g)
            t.set_orientation(choice(["vert", "horiz", "diag"]))
            t.render(self.buf)
            self.add_entity(t)

    def init_scene(self):
        self.add_entity(Sky(0, 0, g))
        self.add_entity(Floor(0, 0, g))
        self.generate_beams()
        self.generate_coins()
        self.add_entity(Magnet(5, 50, g))
        self.add_entity(Dragon(10, 450, g))
        self.mando = Mando(10, 0, g)
        self.add_entity(self.mando)

    def get_time_left(self):
        t = time.time() - self.game_start_time
        assert t >= 0
        return int(self.total_time - t)

    def generate_banner(self):
        t = max(0, self.get_time_left())
        assert t <= 120
        banner = f"Score: {self.score} Lives: {self.mando.lives} Time Left: {t} Shield Cooldown: {60}"
        return banner

    def should_terminate(self):
        return self.get_time_left() <= 0 or not self.is_running

    def run(self):
        self.l = 0
        self.r = self.l + 120
        self.game_start_time = time.time()
        try:
            self.screen.initialize()
            self.init_scene()
            while not self.should_terminate():
                # print(self.l, self.mando.lives, self.input)
                self.process_input()
                self.tick()
                # print("here")
                self.draw(self.l, self.r, self.generate_banner())
                sleep(1 / 30)

                if self.ticks % 5 == 0:
                    self.l = min(self.l + 1, self.col - 120)
                    self.r = min(self.r + 1, self.col)
        except KeyboardInterrupt as ex:
            print(ex)
        finally:
            self.screen.restore()
            os.system("clear")
            print("Game Over!")


if __name__ == "__main__":
    threading.Thread(target=getchar, daemon=True).start()
    colorama.init()
    g = Game()
    g.run()
