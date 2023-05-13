import pygame as pg
from components.Text import Text


class ButtonText(Text):

    def __init__(self,pos_x, pos_y, content, font, text_color, color_active, padding_x=0, padding_y=0, background_color="transparent", border_radius=0):
        super().__init__(pos_x, pos_y, content, font, text_color, padding_x, padding_y, background_color, border_radius=border_radius)
        self.__color_active = color_active
        self.__background_color = background_color

    def handle_mouse_event(self, event):
        point = pg.mouse.get_pos()
        collide = self._rect.collidepoint(point)
        self.color = self.__color_active if collide else self.__background_color
        if collide:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # If Button is left clicked
                return True




    # else: self.color = self.background_color


