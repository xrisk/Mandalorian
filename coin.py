import entity
from colorama import Fore


class Coin(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)

    def tick(self, buf):
        pass

    def hide(self):
        self._show = False

    def render(self, buf):
        if self._show:
            buf[self._x][self._y] = Fore.YELLOW + "$" + Fore.RESET
            self._g._backing[(self._x, self._y)].append(self)
