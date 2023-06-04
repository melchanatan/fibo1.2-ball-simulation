import pygame as pg
from components.Sprite import Sprite


class ButtonIcon(Sprite):

    def __init__(self, *args, alternative_path=None):
        super().__init__(*args)
        self.old_path = self.image_path
        self.alternative_path = alternative_path if alternative_path else self.image_path

    def handle_mouse_event(self, event):
        point = pg.mouse.get_pos()
        collide = self._rect.collidepoint(point)
        if collide:
            self.image_path = self.alternative_path
            self.render()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # If Button is left clicked
                self.scale_image(self.scaling - self.scaling*0.01)  # Animation
                return True
            else:
                self.scale_image(self.scaling)
        else:
            self.image_path = self.old_path
            self.render()


