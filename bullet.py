import entity

import numpy as np
from floor import Floor, Sky
from beam import Beam
import mando


import dragon


class Bullet(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self._rep = np.array([["=", ">"]])
        self._h = 1
        self._w = 2
        self._vy = 2

    def check_collision(self):
        if self._x < 0 or self._x + self._h >= self._g.get_rows():
            self.hide()
            return
        elif (
            self._y < self._g.get_left_col()
            or self._y + self._w >= self._g.get_right_col()
        ):
            self.hide()
            return
        for x in range(self._x, self._x + self._h):
            for y in range(self._y, self._y + self._w):
                for o in self._g._backing[(x, y)]:
                    if not o.is_show():
                        continue
                    elif isinstance(o, Beam):
                        self._g.increment_score(5)
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
        if not self._show:
            return
        self._y += self._vy
        self.check_collision()


class Snowball(Bullet):
    def __init__(self, *args):
        super().__init__(*args)
        self._rep = [["*", "*"], ["*", "*"]]
        self._h = 2
        self._w = 2

    def tick(self, buf):
        if not self._show:
            return

        self._y -= self._vy
        self.check_collision()

    def check_collision(self):
        if self._x < 0 or self._x + self._h >= self._g.get_rows():
            self.hide()
            return
        elif (
            self._y < self._g.get_left_col()
            or self._y + self._w >= self._g.get_right_col()
        ):
            self.hide()
            return
        for x in range(self._x, self._x + self._h):
            for y in range(self._y, self._y + self._w):
                for o in self._g._backing[(x, y)]:
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
