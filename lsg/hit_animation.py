from random import seed, randint
from algoviz.svg import Circle


class HitAnimation:

    def __init__(self, x, line, view, red, green):
        self._red = red
        self._green = green
        self._x = x
        self._y = line * 90 + 76
        self._view = view
        self._group = []
        self.create_circles()
        self._lifetime = 1.0

    def create_circles(self):
        seed()
        for i in range(4):
            x = self._x + randint(10, 60)
            y = self._y + randint(-30, 30)
            r = randint(2, 6)
            new_circle = Circle(x, y, r, self._view)
            new_circle.set_fill_rgb(self._red, self._green, 0)
            new_circle.set_color_rgb(0, 0, 0, 0)
            self._group.append(new_circle)

    def animate(self):
        self._lifetime -= 0.1
        for circle in self._group:
            circle.set_fill_rgb(self._red*self._lifetime, self._green*self._lifetime, 0, self._lifetime)


    def get_lifetime(self):
        return self._lifetime
