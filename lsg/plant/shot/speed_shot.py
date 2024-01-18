from lsg.plant.shot.shot import Shot


class SpeedShot(Shot):
    """Klasse für die Schüsse von der SpeedPlant"""

    def __init__(self, x, y, column, row, view):
        super().__init__(column, row, view)
        self._x += x
        self._y += y
        self._image.move_to(self._x, self._y)
        self._image.set_radius(3)
        self._speed = 15