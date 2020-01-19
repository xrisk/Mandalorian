import entity

import numpy as np


class Mando(entity.Entity):
    rep = np.zeros(shape=(3, 3), dtype=str)
    rep.fill("X")
    h = 3
    w = 3

    def __init__(self, *args):
        super().__init__(*args)
        self.vx = 0
        self.yv = 0

    def tick(self):
        lx, ly = self.x, self.y
        if self.g.input == b"w":
            self.x -= 1
        elif self.g.input == b"a":
            self.y -= 1
            self.x += 1
        elif self.g.input == b"d":
            self.y += 1
            self.x += 1
        elif self.g.input == b"":
            self.x += 1
        if (
            self.x + self.h >= self.g.row
            or self.x < 0
            or self.y < 0
            or self.y + self.w >= self.g.col
        ):
            self.x, self.y = lx, ly
