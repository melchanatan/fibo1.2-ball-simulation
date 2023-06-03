import sys
import os

import pygame as pg
from components.Rectangle import Rectangle
from components.Text import Text
from components.ButtonText import ButtonText
from components.ButtonIcon import ButtonIcon
from components.Sprite import Sprite
from components.DimensionLine import DimensionLine
from components.FileHandler import FileHandler
from components.ProgressBar import ProgressBar
from components.Selector import Selector
from components.Calculator import Calculator

# Initialize Pygame (always on top)
pg.init()

# Initial Variable
BACKGROUND_COLOR = (239, 247, 255)
BACKGROUND_COLOR_300 = (239, 255, 255)
PRIMARY_COLOR_100 = (82, 109, 130)
PRIMARY_COLOR_300 = (84, 91, 119)

FONT_BOLD = pg.font.Font("fonts/Prompt-Bold.ttf", 32)
FONT_BOLD_SMALL = pg.font.Font("fonts/Prompt-Bold.ttf", 24)
FONT_LIGHT_SMALL = pg.font.Font("fonts/Prompt-Regular.ttf", 18)
FONT_SMALL = pg.font.Font("fonts/Prompt-Regular.ttf", 23)
FONT_SUB = pg.font.Font("fonts/MPLUSRounded1c-Bold.ttf", 20)

ROBOT_CONSTANT = 10
MOTOR_CONSTANT_1 = 1
MOTOR_CONSTANT_2 = 2

fps = 60
fpsClock = pg.time.Clock()
pk = 2
screen_width, screen_height = 1280, 720

screen = pg.display.set_mode((screen_width, screen_height))

grid_x = screen_width / 16
grid_y = screen_height / 16
current_step = "simulate"
progress_bar = ProgressBar(screen_width / 2, grid_y + 20, FONT_LIGHT_SMALL, FONT_SUB, status=current_step)

### Setup Page ###
selector = Selector(screen_width / 2, screen_height / 2)
button_next_1 = ButtonText(grid_x * 14 - 40, grid_y * 13 + 30, "next →", FONT_BOLD, BACKGROUND_COLOR, PRIMARY_COLOR_300,
                           background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10, border_radius=20)

### Progress Page ###
resulting_pwm = 10
resulting_rpm = 2100
robot_position_x = 40  # in cm

button_back_2 = ButtonText(grid_x * 1, grid_y * 13 + 30, "Back", FONT_BOLD, PRIMARY_COLOR_300, background_color=BACKGROUND_COLOR,
                           color_active=BACKGROUND_COLOR_300, padding_x=50, padding_y=10, border_radius=20)
button_next_2 = ButtonText(grid_x * 14 - 100, grid_y * 13 + 30, "Simulate", FONT_BOLD, BACKGROUND_COLOR,
                           PRIMARY_COLOR_300, background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10,
                           border_radius=20)

rec_2_1 = Rectangle(grid_x*10 - 100, grid_y*4 + 10, grid_x * 5, grid_y * 3 + 30, "white", border_radius=30)
rec_2_2 = Rectangle(grid_x*10 - 100, grid_y * 8 + 10, grid_x * 5, grid_y * 3 + 30, "white", border_radius=30)

text_pwm = Text(grid_x*10 - 45, grid_y*4 + 25, "PWM", FONT_BOLD, PRIMARY_COLOR_100)
text_pwm_result = Text(grid_x*10 - 45, grid_y*4 + 90, f"{resulting_pwm} V", FONT_BOLD, PRIMARY_COLOR_100)
rec_2_4 = Rectangle(grid_x*10 - 75, grid_y*4 + 70, grid_x*4 + 30, grid_y * 2, PRIMARY_COLOR_100, border_radius=30)
rec_2_5 = Rectangle(grid_x*10 - 75 + 4, grid_y*4 + 70 + 4, grid_x*4 + 30 - 8, grid_y * 2 - 8, "white",
                  border_radius=27)

text_rpm = Text(grid_x*10 - 45, grid_y * 8 + 25, "RPM", FONT_BOLD, PRIMARY_COLOR_100)
text_rpm_result = Text(grid_x*10 - 45, grid_y * 8 + 90, f"{resulting_rpm} RPM", FONT_BOLD, PRIMARY_COLOR_100)
rec_2_6 = Rectangle(grid_x*10 - 75, grid_y * 8 + 70, grid_x*4 + 30, grid_y * 2, PRIMARY_COLOR_100, border_radius=30)
rec_2_7 = Rectangle(grid_x*10 - 75 + 4, grid_y * 8 + 70 + 4, grid_x*4 + 30 - 8, grid_y * 2 - 8, "white",
                  border_radius=27)

rec_2_3 = Rectangle(grid_x*4 - 100, grid_y * 3 + 40, grid_x * 5, grid_x * 5, "white", border_radius=30)

robot_pos_x_in_px = robot_position_x * 324 / 80
field_starting_pos = (grid_x*4 - 63, grid_y * 3 + 85)
field_ending_pos = (field_starting_pos[0] + robot_pos_x_in_px, field_starting_pos[1])

dimension_top = DimensionLine((field_starting_pos[0], field_starting_pos[1]-10), (field_ending_pos[0], field_ending_pos[1]-10))
sprite_field_top = Sprite(field_starting_pos[0], field_starting_pos[1], "graphics/field_top.png", scaling=0.145)
sprite_robot_top = Sprite(field_ending_pos[0], field_starting_pos[1] + 3, "graphics/Topview.png", scaling=0.4)
text_robot_pos_x = Text(field_starting_pos[0]+(field_ending_pos[0]-field_starting_pos[0])/2-33, field_starting_pos[1]-45, f"{robot_position_x} cm", FONT_SMALL, PRIMARY_COLOR_100)

progress_components = [button_back_2, button_next_2, rec_2_1, rec_2_2, rec_2_3, rec_2_4, rec_2_5, text_pwm, text_pwm_result,
                       rec_2_6, rec_2_7, text_rpm, text_rpm_result, sprite_field_top, sprite_robot_top, dimension_top, text_robot_pos_x]

### Simulate Page ###
playback_speed = 1

button_back_3 = ButtonText(grid_x * 1, grid_y * 13 + 30, "Back", FONT_BOLD, PRIMARY_COLOR_300, background_color=BACKGROUND_COLOR,
                           color_active=BACKGROUND_COLOR_300, padding_x=50, padding_y=10, border_radius=20)
button_next_3 = ButtonText(grid_x * 14 - 40, grid_y * 13 + 30, "END", FONT_BOLD, BACKGROUND_COLOR, PRIMARY_COLOR_300,
                           background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10, border_radius=20)
button_plus_playback_speed = ButtonText(screen_width/2-20-60, grid_y * 13 + 30, "-", FONT_BOLD, PRIMARY_COLOR_300, background_color=BACKGROUND_COLOR,
                           color_active=BACKGROUND_COLOR_300, padding_x=34, padding_y=0, border_radius=100)
button_minus_playback_speed = ButtonText(screen_width/2-20+70, grid_y * 13 + 30, "+", FONT_BOLD, PRIMARY_COLOR_300, background_color=BACKGROUND_COLOR,
                           color_active=BACKGROUND_COLOR_300, padding_x=34, padding_y=0, border_radius=100)
text_playback_speed = ButtonText(screen_width/2-20, grid_y * 13 + 25, f"x{playback_speed}", FONT_BOLD_SMALL, BACKGROUND_COLOR, background_color=PRIMARY_COLOR_100, color_active=PRIMARY_COLOR_100,
                           padding_x=34, padding_y=20, border_radius=100)
rec_3_1 = Rectangle(grid_x*2, grid_y*3+20, grid_x * 12, grid_x * 5, "white", border_radius=30)
text_pwm_simulate = Text(grid_x*2 + 45, grid_y*3+40, f"PWM = {resulting_pwm} V", FONT_LIGHT_SMALL, PRIMARY_COLOR_100)
text_rpm_simulate = Text(grid_x*2 + 45, grid_y*3+40+25, f"RPM = {resulting_rpm} RPM", FONT_LIGHT_SMALL, PRIMARY_COLOR_100)

simulate_components = [button_next_3, button_back_3, button_plus_playback_speed, button_minus_playback_speed, text_playback_speed, rec_3_1, text_pwm_simulate, text_rpm_simulate]

target_pos = None
while True:
    screen.fill(BACKGROUND_COLOR)
    progress_bar.draw(screen, status=current_step)
    if current_step == "setup":
        button_next_1.draw(screen)
        selector.draw(screen)
    elif current_step == "progress":
        for component in progress_components:
            component.draw(screen)
    elif current_step == "simulate":
        for component in simulate_components:
            component.draw(screen)

    for event in pg.event.get():

        if current_step == "setup":
            if button_next_1.handle_mouse_event(event) and target_pos != None:
                current_step = "progress"
            selector_event = selector.handle_mouse_event(event)
            target_pos = selector_event if selector_event != None else target_pos

        elif current_step == "progress":
            if button_next_2.handle_mouse_event(event):
                current_step = "simulate"
            if button_back_2.handle_mouse_event(event):
                current_step = "setup"

        elif current_step == "simulate":
            if button_next_3.handle_mouse_event(event):
                current_step = "setup"
            if button_back_3.handle_mouse_event(event):
                current_step = "progress"
            if button_plus_playback_speed.handle_mouse_event(event):
                pass
            if button_minus_playback_speed.handle_mouse_event(event):
                pass

        if event.type == pg.MOUSEBUTTONUP:
            print(pg.mouse.get_pos())
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Update.

    # Draw.

    pg.display.flip()
    fpsClock.tick(fps)
