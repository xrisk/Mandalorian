import entity

import numpy as np
import time

from floor import Floor, Sky
from coin import Coin
from beam import Beam
from bullet import Bullet
from magnet import Magnet


def constrain(val, low, hi):
    if val < low:
        return low
    elif val > hi:
        return hi
    else:
        return val


class Mando(entity.Entity):
    rep = np.zeros(shape=(3, 3), dtype=object)
    rep.fill("X")
    h = 3
    w = 3
    lives = 3

    def __init__(self, *args):
        super().__init__(*args)
        self.vx = 0
        self.vy = 0
        self.real_x = self.x
        self.real_y = self.y
        self.ax = -0.03
        self.gravity = -self.ax / 1.1
        self.last_bullet = None

    def idk(self):
        self.x = round(self.real_x)
        self.y = round(self.real_y)

    def check_collision(self):
        self.idk()
        if self.x < 0 or self.x + self.h >= self.g.row:
            return True
        elif self.y < self.g.l or self.y + self.w >= self.g.r:
            return True
        for x in range(self.x, self.x + self.h):
            for y in range(self.y, self.y + self.w):
                for o in self.g.backing[(x, y)]:
                    if not o.show:
                        continue
                    if (
                        isinstance(o, Floor)
                        or isinstance(o, Sky)
                        or isinstance(o, Magnet)
                    ):
                        return True
                    elif isinstance(o, Beam):
                        self.lives -= 1
                        o.hide()
                # no collision with wall
                # check for coin colls etc
                for o in self.g.backing[(x, y)]:
                    if isinstance(o, Coin):
                        o.hide()
        return False

    def tick(self, buf):

        if self.real_y < self.g.l:
            self.real_y = self.g.l

        lx, ly = self.real_x, self.real_y

        def rollback():
            self.real_x, self.real_y = lx, ly

        attracted = set()
        for x in range(self.x, self.x + self.h):
            for i in range(self.g.l, self.g.r):
                for o in self.g.backing[(x, i)]:
                    if isinstance(o, Magnet):
                        if o in attracted:
                            continue
                        if o.y < self.real_y:
                            self.real_y -= 5 * 1 / abs(o.y - self.real_y)
                            attracted.add(o)
                        elif o.y > self.real_y:
                            self.real_y += 5 * 1 / abs(o.y - self.real_y)
                            attracted.add(o)

        attracted.clear()

        for y in range(self.y, self.y + self.w):
            for i in range(0, self.g.row):
                for o in self.g.backing[(i, y)]:
                    if isinstance(o, Magnet):
                        if o in attracted:
                            continue
                        if o.x < self.real_x:
                            self.real_x -= 5 * 1 / abs(o.x - self.real_x)
                            attracted.add(o)
                        elif o.x > self.real_x:
                            self.real_x += 5 * 1 / abs(o.x - self.real_x)

        if self.g.input == b"w":
            self.vx += self.ax - self.gravity
            self.real_x += self.vx
        elif self.g.input == b"a":
            self.real_y -= 1
            self.vx += self.gravity
            self.real_x += self.vx
        elif self.g.input == b"d":
            self.real_y += 1
            self.vx += self.gravity
            self.real_x += self.vx
        elif self.g.input == b"":
            self.vx += self.gravity
            self.real_x += self.vx
        elif self.g.input == b"q":
            if not self.last_bullet or time.time() - self.last_bullet > 1:
                self.last_bullet = time.time()
                self.g.add_entity(Bullet(self.x, self.y, self.g))

        self.vx = constrain(self.vx, -2, 2)

        if not self.check_collision():
            return

        rollback()

        if self.g.input == b"d":
            self.real_y += 1
            if not self.check_collision():
                return
        elif self.g.input == b"a":
            self.real_y -= 1
            if not self.check_collision():
                return

        rollback()

        # stoppedd
        self.vx = 0

    def render(self, buf):
        self.idk()
        super().render(buf)
