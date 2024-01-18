from lsg.plant.shot.shot import Shot
from algoviz.svg import Circle


class CanonShot(Shot):
    """Schüsse, die von der CanonPlant abgefeuert werden."""

    def __init__(self, column, row, view):
        super().__init__(column, row, view)
        self._color = "Yellow"
        self._image = Circle(self._x, self._y, 10, view)
        self._image.set_fill(self._color)
        self._speed = 30