from algoviz.svg import Image
from random import seed, randrange

class Zombie:  
    
    def __init__(self, row, position, view):
        seed()
        self._line = row
        self._x = 880 + position * 90
        self._y = 31 + (self._line * 90)
        self._view = view
        self._hp = 100
        self._speed = 2
        self._dmg = 40
        self._image = Image("./lsg/media/zombie.png", self._x, self._y, 90, 90, view)
        self._attack_timer = 10
            
    def move(self):
        self._x -= self._speed
        self._image.move_to(self._x, self._y)
        
    def hit(self, dmg):
        self._hp -= dmg
        return self._hp
    
    def in_front_of_plant(self, plants):
        for plant_idx in range(len(plants)):
            if plants[plant_idx] != None:
                plant_x = plants[plant_idx].get_x()
                if plant_x + 90 >= self._x > plant_x:
                    return plant_idx
        else:
            return -1
        
    def get_hp(self):
        return self._hp
    
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_dmg(self):
        return self._dmg
    
    def get_row(self):
        return int(self._line)
    
    def get_attack_timer(self):
        return self._attack_timer
    
    def set_attack_timer(self, new_timer):
        self._attack_timer = new_timer