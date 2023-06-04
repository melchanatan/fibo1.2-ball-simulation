import pygame as pg
from components.Text import Text


class TextWarning(Text):

    def __init__(self, *args, shake_power=1):
        super().__init__(*args)
        self.movement_list = []
        self.shake_power = shake_power
        self.starting_pos_x = self.pos_x
        self.starting_pos_y = self.pos_y
        # self.timer = None

    def shake(self):
        self.movement_list = [1, 1, 2, 2, 3, 3, 4, 4, 1, 1, 2, 2]

    def draw(self, screen):
        try:
            movement_command = self.movement_list.pop(0)
            if movement_command == 1:
                self.pos_x += self.shake_power
            elif movement_command == 2:
                self.pos_x -= self.shake_power
            elif movement_command == 3:
                self.pos_y += self.shake_power
            elif movement_command == 4:
                self.pos_y -= self.shake_power
            self.render()
        except IndexError:
            self.pos_x = self.starting_pos_x
            self.pos_y = self.starting_pos_y
        super().draw(screen)