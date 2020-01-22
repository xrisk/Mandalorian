import entity

import numpy as np
import time

from floor import Floor, Sky
from coin import Coin
from beam import Beam
from bullet import Bullet
from magnet import Magnet
from dragon import Dragon
from colorama import Fore


def constrain(val, low, hi):
    if val < low:
        return low
    elif val > hi:
        return hi
    else:
        return val


class Mando(entity.Entity):
    def read_sprite(self):
        with open("ufo.txt") as f:
            texture = f.readlines()

        texture = [list(s.strip("\r\n")) for s in texture]

        yellow = []
        white = []
        for line in texture:
            tmp = []
            tmp2 = []
            for ch in line:
                tmp.append(Fore.YELLOW + ch + Fore.RESET)
                tmp2.append(Fore.WHITE + ch + Fore.RESET)
            yellow.append(tmp)
            white.append(tmp2)

        self.__noshield_texture = white
        self._rep = self.__noshield_texture

        self.__shield_texture = yellow

        self._h = len(self._rep)
        self._w = len(self._rep[0])

    def __init__(self, *args):
        super().__init__(*args)
        self.read_sprite()
        self.__vx = 0
        self.__vy = 0
        self.__real_x = self._x
        self.__real_y = self._y
        self.__ax = -0.03
        self.__gravity = -self.__ax / 1.1
        self.__last_bullet = None
        self.__lives = 3
        self.__shield = False

    def idk(self):
        self._x = round(self.__real_x)
        self._y = round(self.__real_y)

    def check_collision(self):
        self.idk()
        if self._x < 0 or self._x + self._h >= self._g.get_rows():
            return True
        elif (
            self._y < self._g.get_left_col()
            or self._y + self._w >= self._g.get_right_col()
        ):
            return True
        for x in range(self._x, self._x + self._h):
            for y in range(self._y, self._y + self._w):
                for o in self._g._backing[(x, y)]:
                    if not o.is_show():
                        continue
                    if (
                        isinstance(o, Floor)
                        or isinstance(o, Sky)
                        or isinstance(o, Magnet)
                        or isinstance(o, Dragon)
                    ):
                        return True
                    elif isinstance(o, Beam):
                        self.decrement_life()
                        o.hide()
                # no collision with wall
                # check for coin colls etc
                for o in self._g._backing[(x, y)]:
                    if isinstance(o, Coin):
                        self._g.increment_score(1)
                        o.hide()
        return False

    def get_lives(self):
        return self.__lives

    def tick(self, buf):

        if self.__shield and time.time() - self.__shield_start_time >= 10:
            self.__shield = False

        if self.__real_y < self._g.get_left_col():
            self.__real_y = self._g.get_left_col()

        lx, ly = self.__real_x, self.__real_y

        def rollback():
            self.__real_x, self.__real_y = lx, ly

        attracted = set()
        for x in range(self._x, self._x + self._h):
            for i in range(self._g.get_left_col(), self._g.get_right_col()):
                for o in self._g._backing[(x, i)]:
                    if isinstance(o, Magnet):
                        if o in attracted:
                            continue
                        if o._y < self.__real_y:
                            self.__real_y -= 10 * 1 / abs(o._y - self.__real_y)
                            attracted.add(o)
                        elif o._y > self.__real_y:
                            self.__real_y += 10 * 1 / abs(o._y - self.__real_y)
                            attracted.add(o)

        attracted.clear()

        for y in range(self._y, self._y + self._w):
            for i in range(0, self._g.get_rows()):
                for o in self._g._backing[(i, y)]:
                    if isinstance(o, Magnet):
                        if o in attracted:
                            continue
                        if o._x < self.__real_x:
                            self.__real_x -= 10 * 1 / abs(o._x - self.__real_x)
                            attracted.add(o)
                        elif o._x > self.__real_x:
                            self.__real_x += 10 * 1 / abs(o._x - self.__real_x)

        inp = self._g.get_input()
        if inp == b"w":
            self.__vx += self.__ax - self.__gravity
            self.__real_x += self.__vx
        elif inp == b"a":
            self.__real_y -= 1
            self.__vx += self.__gravity
            self.__real_x += self.__vx
        elif inp == b"d":
            self.__real_y += 1
            self.__vx += self.__gravity
            self.__real_x += self.__vx
        elif inp == b"":
            self.__vx += self.__gravity
            self.__real_x += self.__vx
        elif inp == b"q":
            if not self.__last_bullet or time.time() - self.__last_bullet > 1:
                self.__last_bullet = time.time()
                self._g.add_entity(Bullet(self._x, self._y, self._g))
        elif inp == b" ":
            if (
                not self._g.get_last_shield_time()
                or time.time() - self._g.get_last_shield_time()
                >= self._g.get_shield_cooldown()
            ):
                self.__shield_start_time = time.time()
                self._g.set_last_shield_time(time.time())
                self.__shield = True
        elif inp == b"b":
            self._g.set_fps(200)

        self.__vx = constrain(self.__vx, -2, 2)

        if not self.check_collision():
            return

        rollback()

        if self._g.get_input() == b"d":
            self.__real_y += 1
            if not self.check_collision():
                return
        elif self._g.get_input() == b"a":
            self.__real_y -= 1
            if not self.check_collision():
                return

        rollback()

        # stoppedd
        self.__vx = 0

    def decrement_life(self):
        if not self.__shield:
            self.__lives -= 1
            if self.__lives <= 0:
                self._g.stop_running()

    def render(self, buf):
        self.idk()
        if self.__shield:
            self._rep = self.__shield_texture
            super().render(buf)
        else:
            self._rep = self.__noshield_texture
            super().render(buf)
