from algoviz import AlgoViz
from algoviz.svg import SVGView
from lsg.zombie.zombie import Zombie
from random import seed, randrange
from lsg.menue import GameMenue
from lsg.graphics import Grafik
from lsg.plant.basic_plant import BasicPlant
from lsg.plant.canon_plant import CanonPlant
from lsg.plant.speed_plant import SpeedPlant
from lsg.hit_animation import HitAnimation


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
        self._zombie_amount = 1
        self._game_over = False
        self._killed_all_zombies = False
        self._key = ""
        self._spawned_zombies = 0
        self._zombies_for_win = 25
        self._plant_cooldowns = [0, SpeedPlant.cooldown, CanonPlant.cooldown]
        self._plant_cooldown_text = [None, None, None]
        self._current_plant = 3
        self._last_click = self._game_view.last_click()
        self._animations = []


    def start_game(self):
        """Game loop"""
        while not self._game_over and not self._killed_all_zombies:
            self._key = self._game_view.last_key()
            self.update_graphics()
            self.control_zombies()
            self.control_plants()
            self.collision_shot_zombie()
            self.plant_plant()
            self.animations()
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
        """Erstellt eine Liste zum verwalten der Pflanzen auf den Feldern, und belegt diese mit None vor
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
        if self._spawned_zombies % 5 == 0:
            self._zombie_amount += 1
        seed()
        row = randrange(0, 5)
        pos = len(spawning_zombies[row]) + 1
        new_zombie = Zombie(row, pos, self._game_view)
        self._zombies[row].append(new_zombie)
        AlgoViz.sleep(1)
        return row

    def control_zombies(self):
        """Erschafft ggf. neue Zombies und bewegt alle existierenden vorwärts"""
        if self._zombie_timer <= 0 < self._zombies_for_win:
            spawning_zombies = [[], [], [], [], []]
            for i in range(self._zombie_amount):
                row = self.spawn_zombie(spawning_zombies)
                spawning_zombies[row].append(len(spawning_zombies[row]) + 1)
            self._zombie_timer = 200
        else:
            self._zombie_timer -= 1
        for row in range(len(self._zombies)):
            for zombie in self._zombies[row]:
                plant_idx = zombie.in_front_of_plant(self._plants[row])
                if plant_idx >= 0:
                    self.zombie_attack(zombie, row, plant_idx)
                else:
                    zombie.move()
                AlgoViz.sleep(1)

    def control_plants(self):
        self.update_plant_cooldowns()
        for row in range(len(self._plants)):
            for plant in self._plants[row]:
                if plant is not None:
                    plant.shoot(self._zombies[row])

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
            column = int(x // 90)
            row = int(y // 90)
            return column, row
        else:
            return None, None

    def plant_plant(self):
        """Wenn auf dem zuletzt angeklickten Feld noch keine Pflanze steht, die aktuell ausgewählte platziert,
        oder wenn löschen ausgewählt wir und auf dem Feld eine Pflanze steht, diese gelöscht.

        0 = BasicPlant
        1 = SpeedPlant
        2 = CanonPlant
        3 = Löschen
        """
        (column, row) = self.check_clicked_array()
        if column is not None and row is not None and self._plants[row][column] is None:
            if self._plant_cooldowns[0] <= 0 and self._current_plant == 0:
                new_plant = BasicPlant(column, row, self._game_view)
                self._plants[row][column] = new_plant
                self._plant_cooldowns[0] = BasicPlant.cooldown +1
                self._grafik.cooldown_animation(0)
            elif self._plant_cooldowns[1] <= 0 and self._current_plant == 1:
                new_plant = SpeedPlant(column, row, self._game_view)
                self._plants[row][column] = new_plant
                self._plant_cooldowns[1] = SpeedPlant.cooldown+1
                self._grafik.cooldown_animation(1)
            elif self._plant_cooldowns[2] <= 0 and self._current_plant == 2:
                new_plant = CanonPlant(column, row, self._game_view)
                self._plants[row][column] = new_plant
                self._plant_cooldowns[2] = CanonPlant.cooldown+1
                self._grafik.cooldown_animation(2)
        elif (column is not None and row is not None
              and self._plants[row][column] is not None and self._current_plant == 3):
            self._plants[row][column] = None


    def collision_shot_zombie(self):
        """Kontrolliert, ob von jeder Pflanze die Schüsse mit einem Zombie in der Linie Kollidieren.
        Falls ja, wird dem Zombie der Schaden angerechnet, und der Zombie wird gelöscht, wenn er unter
        oder gleich 0 HP hat. Der Schuss wird von der Funktion check_shot_collision dann gelöscht.
        """
        for row in range(len(self._plants)):
            for plant in self._plants[row]:
                if len(self._zombies[row]) > 0:
                    x = self._zombies[row][0].get_x()
                    if plant is not None and plant.check_shot_collision(x):
                        dmg = plant.get_dmg()
                        hp_left = self._zombies[row][0].hit(dmg)
                        self._animations.append(HitAnimation(x, row, self._game_view, 255, 0))
                        if hp_left <= 0:
                            del self._zombies[row][0]
                            self._zombies_for_win -= 1
                            self._grafik.set_game_score(self._zombies_for_win)
                    AlgoViz.sleep(1)

    def zombie_attack(self, zombie, row, column):
        """Die attackierte Pflanze wird der Schaden abgezogen, und falls die HP danach ≤ 0 sind
        wird die Pflanze gelöscht und die Position in der Liste mit None belegt
        """
        attack_timer = zombie.get_attack_timer()
        if attack_timer <= 0:
            dmg = zombie.get_dmg()
            hp = self._plants[row][column].get_hp()
            hp -= dmg
            plant_x = self._plants[row][column].get_x()
            self._animations.append(HitAnimation(plant_x, row, self._game_view, 0, 255))
            if hp <= 0:
                self._plants[row][column] = None
            else:
                self._plants[row][column].set_hp(hp)
        else:
            attack_timer -= 1
            zombie.set_attack_timer(attack_timer)

    def pause_game(self):
        menue = GameMenue(self._game_view)
        button = menue.get_button()
        if button == "exit":
            self._game_over = True
        del menue

    def all_zombies_killed(self):
        """Gibt True zurück, wenn kein Zombie mehr "Lebt" und alle Zombies für den Win erreicht wurden
        --> sonst False
        """
        if self._zombies_for_win <= 0:
            for i in range(len(self._zombies)):
                if len(self._zombies[i]) > 0:
                    return False
            else:
                return True
        else:
            return False

    def zombie_reached_target(self):
        """Gibt True zurück, wenn mindestens ein Zombie am linken Spielfeld angekommen sind
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

    def update_plant_cooldowns(self):
        for idx in range(len(self._plant_cooldowns)):
            if self._plant_cooldowns[idx] > 0:
                self._plant_cooldowns[idx] -= 1
            elif self._plant_cooldowns[idx] == 0:
                self._grafik.cooldown_over(idx)
                self._grafik.set_plant_cooldown(0, idx)
            if self._plant_cooldowns[idx] % 10 == 0:
                self._grafik.set_plant_cooldown(int(self._plant_cooldowns[idx]) // 10, idx)
            AlgoViz.sleep(1)

    def get_selected_plant(self):
        left_button = self._last_click.left()
        if left_button:
            x = self._last_click.x()
            y = self._last_click.y()
            if (10 <= x <= 55) and (10 <= y <= 220):
                for i in range(4):
                    if (50 * i + 10) <= y <= (50 * i + 55):
                        return i
        return -1

    def update_graphics(self):
        try:
            if 1 <= int(self._key) <= 4:
                key = int(self._key) -1
                if key != self._current_plant:
                    self._current_plant = key
                    self._grafik.select_plant(self._current_plant)
        except:
            pass

    def animations(self):
        for idx in range(len(self._animations)):
            try:
                self._animations[idx].animate()
                if self._animations[idx].get_lifetime() <= 0:
                    del self._animations[idx]
            except:
                pass
            AlgoViz.sleep(2)
