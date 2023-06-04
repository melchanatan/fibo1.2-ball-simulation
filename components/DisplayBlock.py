import pygame as pg
from components.Line import Line
from components.Rectangle import Rectangle
from components.Sprite import Sprite
from components.Text import Text
from components.ButtonText import ButtonText
from math import radians, cos, sin, sqrt
import csv

pg.font.init()
BACKGROUND_COLOR = (239, 247, 255)
PRIMARY_COLOR_100 = (82, 109, 130)
RED_COLOR = (255, 0, 0)
RED_COLOR_300 = (255, 223, 0)
SELECTED_COLOR = (26, 95, 122)
GRAY_COLOR = (138, 127, 127)
FONT_LIGHT_SMALL = pg.font.Font("fonts/Prompt-Bold.ttf", 24)
FONT_BOLD = pg.font.Font("fonts/Prompt-Bold.ttf", 28)
FONT_BOLD_BIG = pg.font.Font("fonts/Prompt-Bold.ttf", 50)


class DisplayBlockManager:

    def __init__(self, pos_x, pos_y, grid_x, grid_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.display_blocks = []

        self.render_block()

    def add_block(self, target_pos):
        with open("target_pos.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(target_pos)
        self.render_block()

    def render_block(self):
        self.display_blocks = []
        with open("target_pos.csv", "r", newline="") as file:
            csv_reader = csv.reader(file, delimiter=",")
            for index, row in enumerate(csv_reader):
                print(row)
                if len(row) != 2:
                    print("invaild")
                real_pos = [int(i) for i in row]
                print(real_pos)
                display_block = DisplayBlock(self.pos_x + self.grid_x * (index * 4.6), self.pos_y, self.grid_x,
                                             self.grid_y, real_pos[0], real_pos[1], index)
                self.display_blocks.append(display_block)

    def draw(self, screen):
        for block in self.display_blocks:
            block.draw(screen)

    def handle_event(self, event):
        for block in self.display_blocks:
            lines = []
            if block.button_delete.handle_mouse_event(event):
                with open("target_pos.csv", "r", newline="") as file:
                    csv_reader = csv.reader(file, delimiter=",")
                    for row in enumerate(csv_reader):
                        if list(row[1]) != [str(block.displaying_x_pos), str(block.displaying_y_pos)]:
                            lines.append(row[1])
                with open("target_pos.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    for i in lines:
                        writer.writerow(i)
                self.render_block()

class DisplayBlock:

    def __init__(self, pos_x, pos_y, grid_x, grid_y, displaying_x_pos, displaying_y_pos, target_number):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.displaying_x_pos = displaying_x_pos
        self.displaying_y_pos = displaying_y_pos
        self.target_number = target_number

        text_target_number = Text(self.pos_x, self.pos_y - 40, f"Target {self.target_number}", FONT_BOLD,
                                  PRIMARY_COLOR_100)
        main_div = Rectangle(self.pos_x, self.pos_y, grid_x * 4 - 43, grid_y * 2 + 20, "white", border_radius=30)
        self.button_delete = ButtonText(self.pos_x, self.pos_y, "                -", FONT_BOLD_BIG, BACKGROUND_COLOR,
                                        color_active=RED_COLOR_300,
                                        background_color=RED_COLOR, padding_x=30, padding_y=33, border_radius=30)
        text_x_pos = Text(self.pos_x + 30, self.pos_y + 12, f"X :   {self.displaying_x_pos} mm", FONT_LIGHT_SMALL,
                          PRIMARY_COLOR_100)
        text_y_pos = Text(self.pos_x + 30, self.pos_y + self.grid_y + 12, f"Y :   {self.displaying_y_pos} mm",
                          FONT_LIGHT_SMALL, PRIMARY_COLOR_100)

        self.components = [self.button_delete, main_div, text_x_pos, text_y_pos, text_target_number]

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)
