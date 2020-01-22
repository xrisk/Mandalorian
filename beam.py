import entity


class Beam(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)

    def set_orientation(self, o):
        self.orientation = o

    def render(self, buf):
        if self.show:
            if self.orientation == "diag":
                for i in range(4):
                    buf[self.x + i][self.y + i] = "*"
                    self.g.backing[(self.x + i, self.y + i)].append(self)
            elif self.orientation == "vert":
                for i in range(4):
                    buf[self.x + i][self.y] = "*"
                    self.g.backing[(self.x + i, self.y)].append(self)
            elif self.orientation == "horiz":
                for i in range(5):
                    buf[self.x][self.y + i] = "*"
                    self.g.backing[(self.x, self.y + i)].append(self)
