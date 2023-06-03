import pygame as pg


class Line:

    def __init__(self, starting_pos, ending_pos, color=(83, 113, 136), thickness=2):
        self.starting_pos = starting_pos
        self.ending_pos = ending_pos
        self.color = color
        self.thickness = thickness

    def draw(self, screen):
        pg.draw.line(screen, self.color, self.starting_pos, self.ending_pos, self.thickness)