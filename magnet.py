import entity


class Magnet(entity.Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self._rep = [list(x) for x in [" ^ ", "< >", " V "]]
        self._w = 3
        self._h = 3
