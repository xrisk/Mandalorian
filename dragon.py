import entity
import numpy as np
from colorama import Fore


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
        self.life = 7

    def tick(self, buf):
        if self.g.mando:
            self.x = constrain(self.g.mando.x - 10, 3, 19)
            # self.y = self.g.mando.y

    def render(self, buf):
        for i in range(self.h):
            for j in range(self.w):
                buf[self.x + i][self.y + j] = (
                    Fore.GREEN + self.rep[i][j] + Fore.RESET
                )
                self.g.backing[(self.x + i, self.y + j)].append(self)
