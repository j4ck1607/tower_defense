from lsg.plant.shot.shot import Shot


class BasicShot(Shot):

    def __init__(self, column, row, view):
        super().__init__(column, row, view)
        self._x = column * 90 + 80 + 250
        self._y = row * 90 + 30 + 31
        self._image.move_to(self._x, self._y)

