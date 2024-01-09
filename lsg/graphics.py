from algoviz.svg import Rect, Image, Text


class Grafik:

    def __init__(self, view):
        self._game_view = view
        self._background = Image("./lsg/media/game_background.png", 0, 0, 977, 512, self._game_view)
        self._game_board = Rect(250, 31, 720, 450, self._game_view)
        self._game_board.set_fill_rgb(0, 0, 0, 0)
        self._game_board.set_color_rgb(0, 0, 0, 0)
        self._game_rows = self.draw_game_rows()
        self._game_score = Text(250, 20, f"You have to kill 25 more zombies to win the Game",
                                self._game_view)
        self._plant_cooldowns = self.visual_cooldown()
        self._cooldowns = [None, None, None]
        self._plant_cooldowns_text = [None, None, None]
        for i in range(1, 3):
            self.cooldown_animation(i)
        self.select_plant(3)

    def draw_game_rows(self, rows=5):
        """Erstellt die quadratischen Spielfelder"""
        game_rows = []
        x = self._game_board.get_x()
        y = self._game_board.get_y()
        for row in range(rows):
            game_row = []
            for column in range(8):
                new_column = Rect(x + column * 90, y + row * 90, 90, 90, self._game_view)
                new_column.set_color_rgb(0, 0, 0, 0)
                if (row + column) % 2 != 0:
                    new_column.set_fill("#76f855")
                else:
                    new_column.set_fill("#58de35")
                game_row.append(new_column)
            game_rows.append(game_row)
        return game_rows

    def get_game_rows(self):
        return self._game_rows

    def set_game_score(self, score):
        if score >= 0:
            self._game_score = Text(250, 20, f"You have to kill {score} more zombies to win the Game",
                                self._game_view)
        else:
            self._game_score = Text(250, 20, f"You have to kill the remaining zombies to win the Game",
                                    self._game_view)

    def visual_cooldown(self):
        rects = []
        for i in range(4):
            new_rect = Rect(10, i * 50 + 10, 45, 45, self._game_view)
            new_rect.set_fill_rgb(255, 255, 255)
            rects.append(new_rect)
        basic_cooldown = Image("./lsg/media/basic_plant.png", 10, 10, 45, 45, self._game_view)
        speed_cooldown = Image("./lsg/media/speed_plant.png", 10, 60, 45, 45, self._game_view)
        canon_cooldown = Image("./lsg/media/canon_plant.png", 10, 110, 45, 45, self._game_view)
        nothing = Image("./lsg/media/red_cross.png", 10, 160, 45, 45, self._game_view)
        return basic_cooldown, speed_cooldown, canon_cooldown, nothing, rects

    def cooldown_animation(self, idx):
        new_rect = Rect(10, idx * 50 + 10, 45, 45, self._game_view)
        new_rect.set_fill_rgb(100, 100, 100, 0.7)
        self._cooldowns[idx] = new_rect

    def cooldown_over(self, idx):
        self._cooldowns[idx] = None

    def set_plant_cooldown(self, cooldown, idx):
        self._plant_cooldowns_text[idx] = Text(60, idx * 50 + 30, f"{cooldown}", self._game_view)

    def select_plant(self, idx):
        for cd in self._plant_cooldowns[4]:
            cd.set_color_rgb(255, 255, 255)
        self._plant_cooldowns[4][idx].set_color_rgb(255, 0, 0)

