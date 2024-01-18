from lsg.animations.animation import Animation


class KnockbackAnimation(Animation):
    """Knockback Animation für Zombies, welche von der Canon Plant getroffen wurden"""

    def __init__(self, view, zombie):
        super().__init__(view)
        zombie.set_moving(False)
        self._zombie = zombie
        self._knockback = 20

    def animate(self):
        self._lifetime -= 0.1
        x = self._zombie.get_x()
        if not self._zombie.is_dead():
            if x >= 970:
                self._knockback = 0
                self._zombie.set_moving(True)
            x += self._knockback
            self._zombie.move_to(x)
            if self._lifetime <= 0:
                self._zombie.set_moving(True)
        else:
            self._lifetime = 0
