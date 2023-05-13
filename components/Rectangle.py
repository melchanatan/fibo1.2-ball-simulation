import pygame as pg

class Rectangle:

    def __init__(self, pos_x, pos_y, width=10, height=10, color=(83, 113, 136), border_radius=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.__height = height
        self.__width = width
        self.color = color
        self.border_radius = border_radius

        self._rect = pg.Rect(pos_x, pos_y, width, height)

    def set_color(self, new_color):
        self.color = new_color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self._rect, border_radius=self.border_radius)