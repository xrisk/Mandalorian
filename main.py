import sys
import numpy as np
from time import sleep

from screen import Screen
from mando import Mando
from entity import Entity

import threading

import time
import os

last_char = b""
lock = threading.Lock()


def getchar():
    global last_char
    last = None
    fd = sys.stdin.fileno()
    while True:
        # sleep(0.1)
        char = os.read(fd, 1)
        if char:
            with lock:
                last_char = char
                last = time.time()
        elif not last or time.time() - last > 0.25:
            with lock:
                last_char = b""


# def getchar():
#     while True:
#         char = sys.stdin.read(1)
#         if char:
#             print(char)


class Game:
    def __init__(self, row=25, col=120):
        self.screen = Screen(row, col)
        self.row = row
        self.col = col
        self.buf = np.zeros(shape=(row, col), dtype=bytes)
        self.scene = []
        self.ticks = 0
        self.input = b""
        self.input_time = 0

    def process_input(self):
        with lock:
            tmp = last_char
        self.input = tmp

    # char = sys.stdin.read(1)
    # self.input = char
    # self.input_time = self.ticks

    def add_entity(self, e):
        self.scene.append(e)

    def tick(self):
        self.ticks += 1
        for entity in self.scene:
            entity.tick()

    def draw(self):
        self.buf.fill(b" ")
        for entity in self.scene:
            entity.render(self.buf)
        self.screen.render(self.buf)

    def init_scene(self):
        self.add_entity(Mando(0, 0, g))

    def run(self):
        try:
            self.screen.initialize()
            self.init_scene()
            while True:
                self.process_input()
                self.tick()
                # print("here")
                self.draw()
                sleep(1 / 30)
        except KeyboardInterrupt as ex:
            print(ex)
        finally:
            self.screen.restore()


if __name__ == "__main__":
    threading.Thread(target=getchar, daemon=True).start()
    g = Game()
    g.run()
