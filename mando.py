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

        self.noshield_texture = np.array(texture)
        self.rep = self.noshield_texture

        yellow = []
        for line in texture:
            tmp = []
            for ch in line:
                tmp.append(Fore.YELLOW + ch + Fore.RESET)
            yellow.append(tmp)

        self.shield_texture = yellow

        self.h = len(self.rep)
        self.w = len(self.rep[0])

    def __init__(self, *args):
        super().__init__(*args)
        self.read_sprite()
        self.vx = 0
        self.vy = 0
        self.real_x = self.x
        self.real_y = self.y
        self.ax = -0.03
        self.gravity = -self.ax / 1.1
        self.last_bullet = None
        self.lives = 3
        self.shield = False

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
                        or isinstance(o, Dragon)
                    ):
                        return True
                    elif isinstance(o, Beam):
                        self.decrement_life()
                        o.hide()
                # no collision with wall
                # check for coin colls etc
                for o in self.g.backing[(x, y)]:
                    if isinstance(o, Coin):
                        self.g.increment_score(1)
                        o.hide()
        return False

    def tick(self, buf):

        if self.shield and time.time() - self.shield_start_time >= 10:
            self.shield = False

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
                            self.real_y -= 10 * 1 / abs(o.y - self.real_y)
                            attracted.add(o)
                        elif o.y > self.real_y:
                            self.real_y += 10 * 1 / abs(o.y - self.real_y)
                            attracted.add(o)

        attracted.clear()

        for y in range(self.y, self.y + self.w):
            for i in range(0, self.g.row):
                for o in self.g.backing[(i, y)]:
                    if isinstance(o, Magnet):
                        if o in attracted:
                            continue
                        if o.x < self.real_x:
                            self.real_x -= 10 * 1 / abs(o.x - self.real_x)
                            attracted.add(o)
                        elif o.x > self.real_x:
                            self.real_x += 10 * 1 / abs(o.x - self.real_x)

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
        elif self.g.input == b" ":
            if (
                not self.g.last_shield_time
                or time.time() - self.g.last_shield_time
                >= self.g.shield_cooldown
            ):
                self.shield_start_time = time.time()
                self.g.last_shield_time = time.time()
                self.shield = True
        elif self.g.input == b"b":
            self.g.fps = 200

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

    def decrement_life(self):
        if not self.shield:
            self.lives -= 1
            if self.lives <= 0:
                self.g.is_running = False

    def render(self, buf):
        self.idk()
        if self.shield:
            self.rep = self.shield_texture
            super().render(buf)
        else:
            self.rep = self.noshield_texture
            super().render(buf)
