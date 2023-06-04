import pygame as pg
from components.Line import Line
from components.Rectangle import Rectangle
from components.Sprite import Sprite
from components.Text import Text
from math import radians, cos, sin, sqrt
import csv
from pathlib import Path


pg.font.init()
BACKGROUND_COLOR = (239, 247, 255)
PRIMARY_COLOR_100 = (33, 50, 94)
SELECTED_COLOR = (26, 95, 122)
GRAY_COLOR = (138, 127, 127)

font_path = Path.cwd() / "fonts"
graphic_path = Path.cwd() / "graphics"

FONT_LIGHT_SMALL = pg.font.Font(font_path / "Prompt-Regular.ttf", 18)

class Selector:

    def __init__(self, pos_x, pos_y, border_radius=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.__circles_display = []
        self.__circles_interactable = []
        self.cm_px = 488/500
        self.__circle_radius = 130 * self.cm_px
        self.circle_border_thickness = 8
        y_pos_calibrate = 187 * self.cm_px

        self.__zero_pos = (pos_x, pos_y + y_pos_calibrate)

        sprite_target_topview = Sprite(pos_x-591.825/2, pos_y-512.46/2, graphic_path / "target_topview.png", .235)
        self.sprite_target_topview = Sprite(pos_x-sprite_target_topview.width*.235/2, pos_y-sprite_target_topview.height*.235/2, "./graphics/target_topview.png", .235)
        # self.sprite_zero_pos = Sprite(self.__zero_pos[0] - 25, self.__zero_pos[1] - 102, "./graphics/XYaxis.png", .05)

        self.__preview_components = {}
        self.__select_components = {}
        self.__select_circle = None

        self.real_data = {}
        self.render()

    def render(self):
        self.__circles_interactable = []
        self.__circles_display = []
        with open(Path.cwd() / "target_pos.csv", "r", newline="") as file:
            csv_reader = csv.reader(file, delimiter=",")
            for index, row in enumerate(csv_reader):
                if len(row) != 2:
                    print("invaild")
                    continue
                real_pos = [int(i) for i in row]
                pos = [round(int(i) / self.cm_px) for i in row]
                circle1 = Rectangle(round(self.__zero_pos[0] + pos[0] - self.__circle_radius / 2),
                                    round(self.__zero_pos[1] + 25 - pos[1] - self.__circle_radius / 2),
                                    self.__circle_radius, self.__circle_radius, color=BACKGROUND_COLOR,
                                    border_radius=100)
                self.__circles_display.append(circle1)
                centers_pos = [
                    round(self.__zero_pos[0] + pos[0] - (self.__circle_radius + self.circle_border_thickness) / 2),
                    round(self.__zero_pos[1] + 25 - pos[1] - (self.__circle_radius + self.circle_border_thickness) / 2)
                ]
                color = PRIMARY_COLOR_100 if centers_pos == self.__select_circle else GRAY_COLOR
                circle2 = Rectangle(
                    centers_pos[0],
                    centers_pos[1],
                    self.__circle_radius + self.circle_border_thickness, self.__circle_radius + self.circle_border_thickness,
                    color=color, border_radius=100)
                self.__circles_interactable.append(circle2)
                self.real_data[circle2] = tuple(real_pos)

    def draw(self, screen):
        self.sprite_target_topview.draw(screen)
        # self.sprite_zero_pos.draw(screen)
        for circle in self.__circles_interactable:
            circle.draw(screen)

        for circle in self.__circles_display:
            circle.draw(screen)

        for item in self.__preview_components.values():
            item.draw(screen)

        for item in self.__select_components.values():
            self.__select_components["center_point"].color = PRIMARY_COLOR_100
            self.__select_components["center_line"].color = PRIMARY_COLOR_100
            self.__select_components["number_text"].set_color(PRIMARY_COLOR_100)
            self.__select_components["number_line"].color = PRIMARY_COLOR_100
            item.draw(screen)

    previewing = True
    def handle_mouse_event(self, event):
        mouse_pos = pg.mouse.get_pos()
        for circle in self.__circles_interactable:
            distance = sqrt((abs(mouse_pos[0]) - abs(circle.pos_x) - self.__circle_radius / 2) ** 2 + (
                    abs(mouse_pos[1]) - abs(circle.pos_y) - self.__circle_radius / 2) ** 2)
            if distance < self.__circle_radius / 2 + 6:
                previewing = True
                # Draw center Line
                circle_center_pos = circle.pos_x + self.__circle_radius / 2 + 2, circle.pos_y + self.__circle_radius / 2 + 2
                self.__preview_components["center_point"] = Rectangle(circle_center_pos[0], circle_center_pos[1], 5, 5, border_radius=100)

                if circle_center_pos[0] - self.__zero_pos[0] + 2 <= 0:
                    line_length = -((500 - (self.__zero_pos[1] - circle_center_pos[1]) / sin(radians(45))) - (
                            self.__zero_pos[0] - circle_center_pos[0]) * 1.4) * .5 - 20
                    line_end = circle_center_pos[0] + line_length * cos(radians(45)), circle_center_pos[
                        1] + line_length * sin(radians(45))

                    self.__preview_components["center_line"] = Line((circle_center_pos[0], circle_center_pos[1]), line_end,
                                                         color=PRIMARY_COLOR_100, thickness=4)
                    number_line_length = 80
                    self.__text_number_preview = Text(line_end[0] - number_line_length, line_end[1] - 27, f"{self.real_data[circle]}", font=FONT_LIGHT_SMALL, text_color=PRIMARY_COLOR_100)
                    number_line_length = self.__text_number_preview.text_width
                    self.__preview_components["number_text"] = Text(line_end[0] - number_line_length, line_end[1] - 27, f"{self.real_data[circle]}", font=FONT_LIGHT_SMALL, text_color=PRIMARY_COLOR_100)
                    self.__preview_components["number_line"] = Line(line_end, (line_end[0] - number_line_length - 3, line_end[1]), color=PRIMARY_COLOR_100, thickness=3)

                else:
                    line_length = -((500 - (self.__zero_pos[1] - circle_center_pos[1]) / sin(radians(45))) - (
                            circle_center_pos[0] - self.__zero_pos[0]) * 1.4) * .5 - 20
                    line_end = circle_center_pos[0] - line_length * cos(radians(45)), circle_center_pos[
                        1] + line_length * sin(radians(45))

                    self.__preview_components["center_line"] = Line((circle_center_pos[0] + 1, circle_center_pos[1] + 2), line_end,
                                                         color=PRIMARY_COLOR_100, thickness=4)
                    text_number = Text(line_end[0], line_end[1] - 27, f"{self.real_data[circle]}", font=FONT_LIGHT_SMALL, text_color=PRIMARY_COLOR_100)
                    self.__preview_components["number_text"] = text_number
                    number_line_length = text_number.text_width
                    self.__preview_components["number_line"] = Line(line_end, (line_end[0] + number_line_length + 3, line_end[1]), color=PRIMARY_COLOR_100, thickness=3)

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.__select_components = self.__preview_components
                    for i in self.__circles_interactable:
                        i.color = GRAY_COLOR
                    circle.color = PRIMARY_COLOR_100
                    self.__select_circle = [circle.pos_x, circle.pos_y]
                    return self.real_data[circle]
                break
        else:
            previewing = False

        if not previewing:
            self.__preview_components = {}
