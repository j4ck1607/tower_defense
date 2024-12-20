from algoviz.svg import Rect, Text


class GameMenue:
    """Diese Klasse erstellt ein Menü, welches dem Spieler die Möglichkeit gibt, das Spiel zu pausieren und
    entweder fortzusetzen oder zu beenden"""

    def __init__(self, view):
        self._view = view
        self._rect_cords = (150, 50, 700, 400)
        self._resume_cords = (200, 100)
        self._exit_cords = (700, 100)
        self._rect = Rect(self._rect_cords[0], self._rect_cords[1], self._rect_cords[2], self._rect_cords[3], view)
        self._resume = Rect(self._resume_cords[0], self._resume_cords[1], 100, 100, view)
        self._exit = Rect(self._exit_cords[0], self._exit_cords[1], 100, 100, view)
        self._resume.set_fill("green")
        self._exit.set_fill("red")
        self._rect.set_fill_rgb(72, 38, 13, 0.95)
        self._text = Text(200, 250, "Press the green button to resume the game,"
                                    " and the red button if you want to exit", view)
        self._button = self.pause_loop()

    def check_click(self, last_click):
        x = last_click.x()
        y = last_click.y()
        if self._resume_cords[0] <= x <= (self._resume_cords[0] + 100) and self._resume_cords[1] <= y <= (
                self._resume_cords[1] + 100):
            return "resume"
        elif self._exit_cords[0] <= x <= (self._exit_cords[0] + 100) and self._exit_cords[1] <= y <= (
                    self._exit_cords[1] + 100):
            return "exit"
        else:
            return "pause"

    def pause_loop(self):
        last_click = self._view.last_click()
        key = self._view.last_key()
        clicked_button = self.check_click(last_click)
        while clicked_button != "resume" and clicked_button != "exit" and key != "Escape":
            last_click = self._view.last_click()
            key = self._view.last_key()
            clicked_button = self.check_click(last_click)
        return clicked_button

    def get_button(self):
        return self._button
