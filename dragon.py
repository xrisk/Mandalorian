import entity
import numpy as np
from colorama import Fore

import bullet
import time


def constrain(val, lo, hi):
    if val < lo:
        return lo
    elif val > hi:
        return hi
    else:
        return val


class Dragon(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)
        with open("dragon.txt") as f:
            self.rep = np.array([list(s[:-1]) for s in f.readlines()])
        self.h = len(self.rep)
        self.w = len(self.rep[0])
        self.life = 1
        self.last_snowball = None

    def decrement_life(self):
        self.life -= 1
        if self.life <= 0:
            self.hide()
            self.g.is_running = False

    def tick(self, buf):
        if not self.last_snowball or time.time() - self.last_snowball > 2:
            self.g.add_entity(bullet.Snowball(self.x + 9, self.y, self.g))
            self.last_snowball = time.time()

    def render(self, buf):
        if self.g.mando:
            self.x = constrain(self.g.mando.x - 10, 3, 19)
        for i in range(self.h):
            for j in range(self.w):
                buf[self.x + i][self.y + j] = (
                    Fore.GREEN + self.rep[i][j] + Fore.RESET
                )
                self.g.backing[(self.x + i, self.y + j)].append(self)
