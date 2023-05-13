import pygame as pg
from components.Sprite import Sprite


class ButtonIcon(Sprite):

    def __init__(self, *args):
        super().__init__(*args)

    def handle_mouse_event(self, event):
        point = pg.mouse.get_pos()
        collide = self._rect.collidepoint(point)
        if collide:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # If Button is left clicked
                self.scale_image(self.scaling - self.scaling*0.01)  # Animation
                return True
            else:
                self.scale_image(self.scaling)


