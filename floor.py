import entity
from colorama import Fore


class Floor(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)

    def render(self, buf):
        row_count = self.g.row
        for col in range(self.g.col):
            for k in range(row_count - 5, row_count):
                buf[k][col] = "-"
                self.g.backing[(k, col)].append(self)


class Sky(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)

    def render(self, buf):
        for col in range(self.g.col):
            for k in range(2):
                buf[k][col] = Fore.BLUE + "~" + Fore.RESET
                self.g.backing[(k, col)].append(self)
