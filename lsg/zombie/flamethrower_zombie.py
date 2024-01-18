from lsg.zombie.zombie import Zombie
from algoviz.svg import Image


class FlamethrowerZombie(Zombie):
    """Der FlamethrowerZombie, welcher einen Flammenwerfer hat, und schneller angreift, als der BasicZombie."""
    attack_timer = 3

    def __init__(self, row, position, view):
        super().__init__(row, position, view)
        self._image = Image("./lsg/media/flamethrower_zombie.png", self._x, self._y, 90, 90, view)
        self._dmg = 6
        self._flame = Image("./lsg/media/flame.png", self._x - 80, self._y + 8, 90, 45, self._view)
        self._index = 1

    def move(self):
        if self._moving:
            self._x -= self._speed
            self._image.move_to(self._x, self._y)
            self._flame.move_to(self._x - 80, self._y + 8)

    def move_to(self, x):
        self._x = x
        self._image.move_to(self._x, self._y)
        self._flame.move_to(self._x - 80, self._y + 8)

    def in_front_of_plant(self, plants):
        for plant_idx in range(len(plants)):
            if plants[plant_idx] is not None:
                plant_x = plants[plant_idx].get_x()
                if plant_x + 150 >= self._x > plant_x - 60:
                    return plant_idx
        else:
            return -1
