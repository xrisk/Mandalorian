import numpy as np


class Entity:
    def __init__(self, x, y, game):
        self._x = x
        self._y = y
        self._show = True
        self._g = game

    def tick(self, buf):
        pass

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def show(self):
        self._show = True

    def hide(self):
        self._show = False

    def is_show(self):
        return self._show

    def render(self, buf):
        try:
            if self._show:
                buf[
                    self._x : self._x + self._h, self._y : self._y + self._w
                ] = self._rep
                for i in range(self._x, self._x + self._h):
                    for j in range(self._y, self._y + self._h):
                        self._g._backing[(i, j)].append(self)
        except Exception as e:
            pass
