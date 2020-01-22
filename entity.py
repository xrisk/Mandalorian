import numpy as np


class Entity:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.show = True
        self.g = game

    def tick(self, buf):
        pass

    def show(self):
        self.show = True

    def hide(self):
        self.show = False

    def render(self, buf):
        try:
            if self.show:
                buf[
                    self.x : self.x + self.h, self.y : self.y + self.w
                ] = self.rep
                for i in range(self.x, self.x + self.h):
                    for j in range(self.y, self.y + self.h):
                        self.g.backing[(i, j)].append(self)
        except Exception as e:
            pass
            print(e)
