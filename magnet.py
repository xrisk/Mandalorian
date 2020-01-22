import entity


class Magnet(entity.Entity):

    rep = [list(x) for x in [" ^ ", "< >", " V "]]
    w = 3
    h = 3

    def __init__(self, *args):
        super().__init__(*args)

    # def render(self, buf):
    #     buf[self.x + self.h, self.y + self.w] = rep
