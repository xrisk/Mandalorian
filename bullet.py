import entity

import numpy as np
from floor import Floor, Sky
from beam import Beam
import mando


import dragon


class Bullet(entity.Entity):

    # vy = 2
    # w = 2
    # h = 1
    # rep = np.array([["=", ">"]])

    def __init__(self, *args):
        super().__init__(*args)
        self.rep = np.array([["=", ">"]])
        self.h = 1
        self.w = 2
        self.vy = 2

    def check_collision(self):
        if self.x < 0 or self.x + self.h >= self.g.row:
            self.hide()
            return
        elif self.y < self.g.l or self.y + self.w >= self.g.r:
            self.hide()
            return
        for x in range(self.x, self.x + self.h):
            for y in range(self.y, self.y + self.w):
                for o in self.g.backing[(x, y)]:
                    if not o.show:
                        continue
                    elif isinstance(o, Beam):
                        self.g.increment_score(5)
                        o.hide()
                        self.hide()
                        return
                    elif isinstance(o, dragon.Dragon):
                        o.decrement_life()
                        self.hide()
                        return
                # no collision with wall
                # check for coin colls etc
        return False

    def tick(self, buf):
        if not self.show:
            return
        self.y += self.vy
        self.check_collision()


class Snowball(Bullet):
    def __init__(self, *args):
        super().__init__(*args)
        self.rep = [["*", "*"], ["*", "*"]]
        self.h = 2
        self.w = 2

    def tick(self, buf):
        if not self.show:
            return

        self.y -= self.vy
        self.check_collision()

    def check_collision(self):
        if self.x < 0 or self.x + self.h >= self.g.row:
            self.hide()
            return
        elif self.y < self.g.l or self.y + self.w >= self.g.r:
            self.hide()
            return
        for x in range(self.x, self.x + self.h):
            for y in range(self.y, self.y + self.w):
                for o in self.g.backing[(x, y)]:
                    if not o.show:
                        continue
                    if isinstance(o, Floor) or isinstance(o, Sky):
                        self.hide()
                        continue
                    elif isinstance(o, mando.Mando):
                        o.decrement_life()
                        self.hide()
                        return
                # no collision with wall
                # check for coin colls etc
        return False
