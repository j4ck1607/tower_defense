from lsg.zombie.zombie import Zombie
from algoviz.svg import Image


class BasicZombie(Zombie):
    attack_timer = 20

    def __init__(self, row, position, view):
        super().__init__(row, position, view)
        self._image = Image("./lsg/media/basic_zombie.png", self._x, self._y, 90, 90, view)
        self._index = 0
