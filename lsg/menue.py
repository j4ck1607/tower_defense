from algoviz.svg import SVGView, Rect, Image, Text

class Game_menue:
    
    def __init__(self, view):
        self._view = view
        self._rect_cords = (150, 50, 700, 400)
        self._resume_cords = (300, 100)
        self._exit_cords = (300, 150)
        self._rect = Rect(self._rect_cords[0], self._rect_cords[1], self._rect_cords[2], self._rect_cords[3], view)
        self._resume = Text(self._resume_cords[0], self._resume_cords[1],"Resume Game",  view)
        self._exit = Text(self._exit_cords[0], self._exit_cords[1],"Exit Game",  view)
        self._rect.set_fill_rgb(72, 38, 13, 0.95)
        self._view.wait_for_click()
        
        
    def still_paused(self):
        resume = self.clicked_resume()
        if resume:
            return False
        else:
            return True
        
    def game_exit(self):
        exit = self.clicked_exit()
        if exit:
            return True
        else:
            return False
            
    def clicked_exit(self):
        last_click = self._view.last_click()
        x = last_click.x()
        y = last_click.y()
        if self._exit_cords[0] <= x <= (self._exit_cords[0]+200) and self._exit_cords[1] <= y <= (self._exit_cords[1]+50):
            return True
        else:
            return False
        
    def clicked_resume(self):
        last_click = self._view.last_click()
        x = last_click.x()
        y = last_click.y()
        if self._resume_cords[0] <= x <= (self._resume_cords[0]+200) and self._resume_cords[1] <= y <= (self._resume_cords[1]+50):
            return True
        else:
            return False