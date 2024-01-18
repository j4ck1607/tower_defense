from random import seed, randint
from algoviz.svg import Circle


class Animation:
    """Eltern Klasse für alle Animationen"""

    def __init__(self, view):
        self._view = view
        self._lifetime = 1.0

    def animate(self):
        self._lifetime -= 0.1

    def get_lifetime(self):
        return self._lifetime
