from algoviz.svg import Image
from lsg.plant.plant import Plant
from lsg.plant.shot.speed_shot import SpeedShot


class SpeedPlant(Plant):
    shot_timer = 20
    cooldown = 50

    def __init__(self, column, row, view):
        super().__init__(column, row, view)
        self._image = Image("./lsg/media/speed_plant.png", self._x, self._y, 90, 90, view)
        self._dmg = 10
        self._shot_timer = SpeedPlant.shot_timer

    def shoot(self, zombies):
        if self._shot_timer <= 0 and (len(zombies) > 0):
            for i in range(-1, 2):
                new_shot = SpeedShot(abs(i) * 15, i * 20, self._column, self._row, self._view)
                self._shots.append(new_shot)
            self._shot_timer = SpeedPlant.shot_timer
        else:
            self._shot_timer -= 1
        self.move_shots()
