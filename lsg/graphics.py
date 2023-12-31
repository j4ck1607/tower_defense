from algoviz.svg import Rect, Image, Text

class Grafik():

    def __init__(self, view):
        self._game_view = view
        self._background = Image("./lsg/media/game_background.png", 0, 0, 977, 512, self._game_view)
        self._game_board = Rect(250, 31, 720, 450, self._game_view)
        self._game_board.set_fill_rgb(0,0,0,0)
        self._game_board.set_color_rgb(0,0,0,0)
        self._game_rows = self.draw_game_rows()
        self._game_score = Text(250, 20,f"You have to kill 25 more zombies to win the Game",
                                self._game_view)
        self._plant_cooldown = Text(0, 20,f" Plantcooldown: 0", self._game_view)

    def draw_game_rows(self, rows = 5):
        """Erstellt die quadratischen Spielfelder"""
        game_rows = []
        x = self._game_board.get_x()
        y = self._game_board.get_y()
        for row in range(rows):
            game_row = []
            for column in range(8):
                new_column = Rect(x + column*90, y + row*90, 90, 90, self._game_view)
                new_column.set_color_rgb(0,0,0,0)
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
        self._game_score = Text(250, 20, f"You have to kill {score} more zombies to win the Game",
                                self._game_view)

    def set_plant_cooldown(self, cooldown):
        self._plant_cooldown = Text(0, 20, f" Plantcooldown: {cooldown}", self._game_view)