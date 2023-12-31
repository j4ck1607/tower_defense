from algoviz import AlgoViz
from algoviz.svg import SVGView, Text
from lsg.zombie import Zombie
from random import seed, randrange
from lsg.plant import Plant
from lsg.menue import Game_menue
from lsg.graphics import Grafik

class Game:
    
    def __init__(self):
        """Erstellt ein neues Plants vs Zombies spiel"""
        AlgoViz.clear()
        seed()
        self._game_view = SVGView(977, 512, "Plants vs Zombies")
        self._grafik = Grafik(self._game_view)
        self._game_rows = self._grafik.get_game_rows()
        self._zombies = [[], [], [], [], []]
        self._plants = self.create_plant_list()
        self._zombie_timer = 50
        self._zombie_amount = 0
        self._game_over = False
        self._killed_all_zombies = False
        self._key = ""
        self._spawned_zombies = 0
        self._zombies_for_win = 25

        # Debug variablen
    
    def start_game(self):
        """Game loop"""
        while not self._game_over and not self._killed_all_zombies:
            self._key = self._game_view.last_key()
            self.control_zombies()
            self.control_plants()
            self.collision_shot_zombie()
            self.plant_plant()
            if self.all_zombies_killed():
                self._killed_all_zombies = True
            elif self.zombie_reached_target():
                self._game_over = True
            if self._key == "Escape":
                self.pause_game()
            AlgoViz.sleep(1)
        if self._game_over:
            print("Verloren! Die Zombies haben dich erreicht!")
        elif self._killed_all_zombies:
            print("Gewonnen! Du hast alle Zombies getötet!")
    
    def create_plant_list(self):
        """Erstellt eine Liste zum verwalten der Pflanzen auf den Felder, und belegt diese mit None vor
        """
        plants = []
        for i in range(len(self._game_rows)):
            plant_rows = []
            for idx in range(len(self._game_rows[i])):
                plant_rows.append(None)
            plants.append(plant_rows)
        return plants
    
    def spawn_zombie(self, spawning_zombies):
        """Erstellt einen neuen Zombie und hängt diesen der Liste an"""
        self._spawned_zombies += 1        
        seed()
        row = randrange(0,5)
        pos = len(spawning_zombies[row])+1
        new_zombie = Zombie(row, pos, self._game_view)
        self._zombies[row].append(new_zombie)
        AlgoViz.sleep(1)
        return row
        
    def control_zombies(self):
        """Erschafft ggf. neue Zombies und bewegt alle existierenden vorwärts"""
        if self._zombie_timer <= 0 and self._zombies_for_win > 0:
            if self._spawned_zombies % 5 == 0:
                self._zombie_amount += 1
            spawning_zombies = [[],[],[],[],[]]
            for i in range(self._zombie_amount):
                row = self.spawn_zombie(spawning_zombies)
                spawning_zombies[row].append(len(spawning_zombies[row])+1)
            self._zombie_timer = 200
        else:
            self._zombie_timer -= 1
        for row in range(len(self._zombies)):
            for zombie in self._zombies[row]:
                plant_idx = zombie.in_front_of_plant(self._plants[row])
                if  plant_idx >= 0:
                    self.zombie_attack(zombie, row, plant_idx)
                else:
                    zombie.move()
                AlgoViz.sleep(1)
                
    def control_plants(self):
        self.update_plant_cooldown()
        for i in range(len(self._plants)):
            for plant in self._plants[i]:
                if plant != None:
                    plant.shoot()
            
    def check_clicked_array(self):
        """Schaut, ob die zuletzt geklickte Position auf dem Spielfeld war,
        und gibt dann die Reihe und Spalte zurück --> sonst None, None
        """
        last_click = self._game_view.last_click()
        x = last_click.x()
        y = last_click.y()
        left_button = last_click.left()
        if left_button and (250 <= x <= 970) and (31 <= y <= 481):
            x -= 250            
            y -= 31
            column = int(x//90)
            row = int(y//90)
            return(column, row)
        else:
            return(None, None)
        
    def plant_plant(self):
        """Wenn auf dem zuletzt angeklickten Feld noch keine Pflanze steht, wird dort eine platziert
        """
        (column, row) = self.check_clicked_array()
        if column != None and row != None and self._plants[row][column] == None and Plant.cooldown <= 0:
            new_plant = Plant(column, row, self._game_view)
            self._plants[row][column] = new_plant
            Plant.cooldown = 151
            
    def collision_shot_zombie(self):
        """Kontrolliert ob von jeder Pflanze die Schüsse mit einem Zombie in der Linie Kollidieren.
        Falls ja, wird dem Zombie der Schaden angerechnet, und der Zombie wird gelöscht wenn er unter oder gleich 0 HP hat
        Der Schuss wird von der Funktion check_shot_collision dann gelöscht.
        for row in range(len(self._plants)):
            for plant in self._plants[row]:
                for zombie_idx in range(len(self._zombies[row])):
                    x = self._zombies[row][zombie_idx].get_x()
                    if plant != None and plant.check_shot_collision(x):
                        dmg = plant.get_dmg()
                        hp_left = self._zombies[row][zombie_idx].hit(dmg)
                        if hp_left <= 0:
                            del self._zombies[row][zombie_idx]
                            self._zombies_for_win -= 1
                            self._zombie_killcount += 1
                    AlgoViz.sleep(1)
        """
        for row in range(len(self._plants)):            
            for plant in self._plants[row]: 
                if len(self._zombies[row]) > 0:
                    x = self._zombies[row][0].get_x()
                    if plant != None and plant.check_shot_collision(x):
                        dmg = plant.get_dmg()
                        hp_left = self._zombies[row][0].hit(dmg)
                        if hp_left <= 0:
                            del self._zombies[row][0]
                            self._zombies_for_win -= 1
                            self._grafik.set_game_score(self._zombies_for_win)
                    AlgoViz.sleep(1)
                    
    def zombie_attack(self, zombie, row, column):
        """Die attackierte Pflanze wird der Schaden abgezogen, und falls die HP danach <= 0 sind
        wird die Pflanze gelöscht und die Position in der Liste mit None belegt
        """
        attack_timer = zombie.get_attack_timer()
        if attack_timer <= 0:
            dmg = zombie.get_dmg()
            hp = self._plants[row][column].get_hp()
            hp -= dmg
            if hp <= 0:
                old_plant = self._plants[row][column]
                self._plants[row][column] = None
                del old_plant
            else:
                self._plants[row][column].set_hp(hp)
        else:
            attack_timer -= 1
            zombie.set_attack_timer(attack_timer)
            
    def pause_game(self):
        game_paused = True
        menue = Game_menue(self._game_view)
        while game_paused:
            if not menue.still_paused():
                game_paused = False
            if menue.game_exit():
                self._game_over = True
                game_paused = False
        del menue
        
    def all_zombies_killed(self):
        """Gibt True zurück wenn kein Zombie mehr "Lebt" und alle Zombies für den Win erreicht wurden
        -->sonst False
        """
        if self._zombies_for_win <= 0:
            zombie_living = False
            for i in range(len(self._zombies)):
                if len(self._zombies[i]) > 0:
                    return False
            else:
                return True
        
    def zombie_reached_target(self):
        """Gibt True zurück wenn mindestens ein Zombie am linken Spielfeld angekommen sind
        --> sonst False
        """
        for i in range(len(self._zombies)):
            for zombie in self._zombies[i]:
                x = zombie.get_x()
                target_x = 250
                if x <= target_x:
                    return True
                AlgoViz.sleep(1)
        else:
            return False
        
    def update_plant_cooldown(self):
        if Plant.cooldown > 0:
            Plant.cooldown -= 1
        elif Plant.cooldown == 0:
            self._grafik.set_plant_cooldown(0)
            Plant.cooldown = -1
        if Plant.cooldown % 10 == 0:
            self._grafik.set_plant_cooldown(int(Plant.cooldown)//10)