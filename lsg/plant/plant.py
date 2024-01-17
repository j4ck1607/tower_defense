from lsg.plant.shot.shot import Shot
from algoviz import AlgoViz


class Plant:

    def __init__(self, column, row, view):
        self._x = column * 90 + 250
        self._y = row * 90 + 31
        self._column = column
        self._row = row
        self._view = view
        self._shots = []
        self._shot_timer = 45
        self._dmg = 25
        self._hp = 100
        self._effect = False

    def get_dmg(self):
        return self._dmg

    def get_hp(self):
        return self._hp

    def get_x(self):
        return self._x

    def set_hp(self, new_hp):
        self._hp = new_hp

    def shoot(self, zombies):
        if self._shot_timer <= 0 and (len(zombies) > 0):
            new_shot = Shot(self._column, self._row, self._view)
            self._shots.append(new_shot)
            self._shot_timer = 45
        else:
            self._shot_timer -= 1
        self.move_shots()

    def move_shots(self):
        if len(self._shots) > 0 and self._shots[0].get_x() >= 970:
            del self._shots[0]
        for shot in self._shots:
            shot.move()
            AlgoViz.sleep(1)

    def check_shot_collision(self, zombie_x):
        try:
            if self._shots[0].get_x() >= zombie_x:
                del self._shots[0]
                return True
            else:
                return False
        except:
            return False

    def has_effect(self):
        return self._effect

    def effect(self, zombie):
        return False

    def delete_shots(self):
        for shot in self._shots:
            self._shots.remove(shot)
