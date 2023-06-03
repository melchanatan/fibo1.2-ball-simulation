import pygame as pg
from components.Line import Line
from components.Rectangle import Rectangle
from components.Sprite import Sprite
from components.Text import Text
from math import radians, cos, sin, sqrt
import csv

pg.font.init()
BACKGROUND_COLOR = (239, 247, 255)
PRIMARY_COLOR_100 = (33, 50, 94)
SELECTED_COLOR = (26, 95, 122)
FONT_LIGHT_SMALL = pg.font.Font("fonts/Prompt-Regular.ttf", 18)


class Selector:

    def __init__(self, pos_x, pos_y, border_radius=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.__circles_display = []
        self.__circles_interactable = []
        self.size = 300
        cm_px = 500 / 550
        self.__circle_radius = 130 * cm_px
        circle_border_thinkness = 8
        y_pos_calibate = 230 * cm_px

        self.__zero_pos = (pos_x, pos_y + y_pos_calibate)

        self.sprite_zero_pos = Sprite(self.__zero_pos[0] - 25, self.__zero_pos[1]-102, "./graphics/XYaxis.png", .05)

        self.__preview_components = {}
        self.__select_components = {}

        self.real_data = {}

        with open("target_pos.csv", "r", newline="") as file:
            csv_reader = csv.reader(file, delimiter=",")
            for row in csv_reader:
                if not row or len(row[0].split(" ")) != 2:
                    print("invalid!")
                    continue
                real_pos = [int(i) for i in row[0].split(" ")]
                pos = [round(int(i) / cm_px) for i in row[0].split(" ")]
                circle1 = Rectangle(round(self.__zero_pos[0] + pos[0] - self.__circle_radius / 2),
                                    round(self.__zero_pos[1] + 25 - pos[1] - self.__circle_radius / 2),
                                    self.__circle_radius, self.__circle_radius, color=BACKGROUND_COLOR,
                                    border_radius=100)
                self.__circles_display.append(circle1)


                circle2 = Rectangle(
                    round(self.__zero_pos[0] + pos[0] - (self.__circle_radius + circle_border_thinkness) / 2),
                    round(self.__zero_pos[1] + 25 - pos[1] - (self.__circle_radius + circle_border_thinkness) / 2),
                    self.__circle_radius + circle_border_thinkness, self.__circle_radius + circle_border_thinkness,
                    color=PRIMARY_COLOR_100, border_radius=100)
                self.__circles_interactable.append(circle2)
                self.real_data[circle2] = tuple(real_pos)

        triangle = self.makeTriangle(self.size, 42)
        self.offsetTriangle(triangle, pos_x, pos_y + 100)

        self.line1 = Line(starting_pos=triangle.p1, ending_pos=triangle.p2, color=PRIMARY_COLOR_100, thickness=3)
        self.line2 = Line(starting_pos=triangle.p2, ending_pos=triangle.p3, color=PRIMARY_COLOR_100, thickness=3)
        self.line3 = Line(starting_pos=triangle.p3, ending_pos=triangle.p1, color=PRIMARY_COLOR_100, thickness=3)

    def draw(self, screen):
        self.line1.draw(screen)
        self.line2.draw(screen)
        self.line3.draw(screen)
        self.sprite_zero_pos.draw(screen)

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

    previewing = False
    def handle_mouse_event(self, event):
        mouse_pos = pg.mouse.get_pos()
        for circle in self.__circles_interactable:
            distance = sqrt((abs(mouse_pos[0]) - abs(circle.pos_x) - self.__circle_radius / 2) ** 2 + (
                    abs(mouse_pos[1]) - abs(circle.pos_y) - self.__circle_radius / 2) ** 2)
            if distance < self.__circle_radius / 2 + 3:
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
                    return self.real_data[circle]

                break
        else:
            previewing = False

        if not previewing:
            self.__preview_components = {}

    def makeTriangle(self, scale, internalAngle):
        # define the points in a uint space
        ia = (radians(internalAngle) * 2) - 1
        p1 = (0, -1)
        p2 = (cos(ia), sin(ia))
        p3 = (cos(ia) * -1, sin(ia))

        # scale the points
        sp1 = [p1[0] * scale, p1[1] * scale]
        sp2 = [p2[0] * scale, p2[1] * scale]
        sp3 = [p3[0] * scale, p3[1] * scale]

        return Triangle(sp1, sp2, sp3)

    def offsetTriangle(self, triangle, offsetx, offsety):
        triangle.p1[0] += offsetx;
        triangle.p1[1] += offsety;
        triangle.p2[0] += offsetx;
        triangle.p2[1] += offsety;
        triangle.p3[0] += offsetx;
        triangle.p3[1] += offsety;


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
