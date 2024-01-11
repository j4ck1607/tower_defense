from lsg.animations.animation import Animation


class KnockbackAnimation(Animation):

    def __init__(self, view, zombie):
        super().__init__(view)
        zombie.set_moving(False)
        self._zombie = zombie
        self._knockback = 20

    def animate(self):
        self._lifetime -= 0.1
        x = self._zombie.get_x()
        if x >= 970:
            self._knockback = 0
            self._zombie.set_moving(True)
        x += self._knockback
        self._zombie.move_to(x)
        if self._lifetime <= 0:
            self._zombie.set_moving(True)
