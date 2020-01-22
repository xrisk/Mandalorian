import entity
from colorama import Fore


class Beam(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)

    def set_orientation(self, o):
        self.__orientation = o

    def render(self, buf):
        if self._show:
            if self.__orientation == "diag":
                for i in range(4):
                    buf[self._x + i][self._y + i] = Fore.RED + "*" + Fore.RESET
                    self._g._backing[(self._x + i, self._y + i)].append(self)
            elif self.__orientation == "vert":
                for i in range(4):
                    buf[self._x + i][self._y] = Fore.RED + "*" + Fore.RESET
                    self._g._backing[(self._x + i, self._y)].append(self)
            elif self.__orientation == "horiz":
                for i in range(5):
                    buf[self._x][self._y + i] = Fore.RED + "*" + Fore.RESET
                    self._g._backing[(self._x, self._y + i)].append(self)
