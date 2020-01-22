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
            self._rep = np.array([list(s[:-1]) for s in f.readlines()])
        self._h = len(self._rep)
        self._w = len(self._rep[0])
        self.__life = 3
        self.__last_snowball = None

    def decrement_life(self):
        self.__life -= 1
        if self.__life <= 0:
            self.hide()
            self._g.do_win()

    def tick(self, buf):
        if not self.__last_snowball or time.time() - self.__last_snowball > 2:
            self._g.add_entity(bullet.Snowball(self._x + 9, self._y, self._g))
            self.__last_snowball = time.time()

    def render(self, buf):
        mando = self._g.get_mando()
        if mando:
            self._x = constrain(mando.get_x() - 10, 3, 19)
        for i in range(self._h):
            for j in range(self._w):
                buf[self._x + i][self._y + j] = (
                    Fore.GREEN + self._rep[i][j] + Fore.RESET
                )
                self._g._backing[(self._x + i, self._y + j)].append(self)
