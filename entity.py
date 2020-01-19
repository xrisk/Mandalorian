import numpy as np


class Entity:

    rep = np.array([["X"]])
    h = 1
    w = 1

    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.show = True
        self.g = game

    def tick(self):
        pass

    def show(self):
        self.show = True

    def hide(self):
        self.show = False

    def render(self, buf):
        if self.show:
            buf[
                self.x : self.x + self.h,  # noqa: E203
                self.y : self.y + self.w,  # noqa: E203
            ] = self.rep
