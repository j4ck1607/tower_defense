from algoviz.svg import Circle

class Shot:
    
    def __init__(self, column, row, view):
        self._speed = 5
        self._x = column*90+80+250
        self._y = row*90+30+31
        self._color = "#93cf2f"
        self._image = Circle(self._x, self._y, 5, view)        
        self._image.set_fill(self._color)
    
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_speed(self):
        return self._speed
    
    def move(self):
        self._x += self._speed
        self._image.move_to(self._x, self._y)