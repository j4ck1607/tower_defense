from algoviz.svg import Image
from lsg.plant.plant import Plant
from lsg.plant.shot.basic_shot import BasicShot


class BasicPlant(Plant):
    shot_timer = 45
    cooldown = 200

    def __init__(self, column, row, view):
        super().__init__(column, row, view)
        self._image = Image("./lsg/media/basic_plant.png", self._x, self._y, 90, 90, view)

    def shoot(self, zombies):
        if self._shot_timer <= 0 and (len(zombies) > 0):
            new_shot = BasicShot(self._column, self._row, self._view)
            self._shots.append(new_shot)
            self._shot_timer = 45
        else:
            self._shot_timer -= 1
        self.move_shots()
