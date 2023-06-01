import pygame as pg
from components.Line import Line


class DimensionLine(Line):

    def __init__(self, *args):
        super().__init__(*args)

    def draw(self, screen):
        if self.starting_pos[1] == self.ending_pos[1]:  #horizontal line
            pg.draw.line(screen, start_pos=self.starting_pos, end_pos=self.ending_pos, color=self.color, width=self.thickness)
            pg.draw.line(screen, start_pos=(self.starting_pos[0], self.starting_pos[1]-self.thickness*2.2), end_pos=(self.starting_pos[0], self.ending_pos[1]+self.thickness*2.2),color=self.color, width=self.thickness)
            pg.draw.line(screen, start_pos=(self.ending_pos[0], self.starting_pos[1]-self.thickness*2.2), end_pos=(self.ending_pos[0], self.ending_pos[1]+self.thickness*2.2),color=self.color, width=self.thickness)
        if self.starting_pos[0] == self.ending_pos[0]:
            pg.draw.line(screen, start_pos=self.starting_pos, end_pos=self.ending_pos, color=self.color,
                         width=self.thickness)
            pg.draw.line(screen, start_pos=(self.starting_pos[0] - self.thickness*2.2, self.starting_pos[1]),
                         end_pos=(self.starting_pos[0] + self.thickness*2.2, self.starting_pos[1]), color=self.color,
                         width=self.thickness)
            pg.draw.line(screen, start_pos=(self.ending_pos[0] - self.thickness*2.2, self.ending_pos[1]),
                         end_pos=(self.ending_pos[0] + self.thickness*2.2, self.ending_pos[1]), color=self.color,
                         width=self.thickness)