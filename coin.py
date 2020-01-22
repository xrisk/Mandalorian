import entity
from colorama import Fore


class Coin(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)

    def tick(self, buf):
        pass

    def hide(self):
        self.show = False

    def render(self, buf):
        if self.show:
            buf[self.x][self.y] = Fore.YELLOW + "$" + Fore.RESET
            self.g.backing[(self.x, self.y)].append(self)
