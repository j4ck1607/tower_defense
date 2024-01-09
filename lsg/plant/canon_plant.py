from algoviz.svg import Image
from lsg.plant.plant import Plant
from lsg.plant.shot.canon_shot import CanonShot


class CanonPlant(Plant):
    shot_timer = 60
    cooldown = 60
    def __init__(self, column, row, view):
        super().__init__(column, row, view)
        self._image = Image("./lsg/media/canon_plant.png", self._x, self._y, 90, 90, view)
        self._shot_timer = CanonPlant.shot_timer
        self._dmg = 80

    def shoot(self, zombies):
        if self._shot_timer <= 0 and (len(zombies) > 0):
            new_shot = CanonShot(self._column, self._row, self._view)
            self._shots.append(new_shot)
            self._shot_timer = CanonPlant.shot_timer
        else:
            self._shot_timer -= 1
        self.move_shots()
