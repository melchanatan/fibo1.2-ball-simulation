import sys
import os
import time
from pathlib import Path

import pygame as pg
from components.Rectangle import Rectangle
from components.Text import Text
from components.ButtonText import ButtonText
from components.ButtonIcon import ButtonIcon
from components.Sprite import Sprite
from components.DimensionLine import DimensionLine
from components.ProgressBar import ProgressBar
from components.Selector import Selector
from components.Calculator import Calculator
from components.Line import Line
from components.InputBox import TextInputBox
from components.DisplayBlock import DisplayBlockManager
from components.Field import Field
from components.Ball import Ball
from components.TextWarning import TextWarning

# Initialize Pygame (always on top)
pg.init()

# Initial Variable
BACKGROUND_COLOR = (239, 247, 255)
BACKGROUND_COLOR_300 = (239, 255, 255)
PRIMARY_COLOR_100 = (82, 109, 130)
PRIMARY_COLOR_300 = (84, 91, 119)
GRAY_COLOR = (205, 215, 228)
WARNING_COLOR = (255, 0, 0)

font_path = Path.cwd() / "fonts"
graphic_path = Path.cwd() / "graphics"

FONT_BOLD = pg.font.Font(font_path / "Prompt-Bold.ttf", 32)
FONT_BOLD_BIG = pg.font.Font(font_path / "Prompt-Bold.ttf", 50)
FONT_BOLD_SMALL = pg.font.Font(font_path / "Prompt-Bold.ttf", 24)
FONT_LIGHT_SMALL = pg.font.Font(font_path / "Prompt-Regular.ttf", 18)
FONT_SMALL = pg.font.Font(font_path / "Prompt-Regular.ttf", 23)
FONT_SUB = pg.font.Font(font_path / "MPLUSRounded1c-Bold.ttf", 20)
FONT_WARNING = pg.font.Font(font_path / "Prompt-Regular.ttf", 20)

ROBOT_CONSTANT = 10
MOTOR_CONSTANT_1 = 1
MOTOR_CONSTANT_2 = 2
GRAVITY = 9.81
INITIAL_THETA = 60

ANIMATION_SPEED = 9

fps = 60
fpsClock = pg.time.Clock()
pk = 2
screen_width, screen_height = 1280, 720

screen = pg.display.set_mode((screen_width, screen_height))

grid_x = screen_width / 16
grid_y = screen_height / 16
current_step = "setup"
progress_bar = ProgressBar(screen_width / 2, grid_y, FONT_LIGHT_SMALL, FONT_SUB, status=current_step)

grid_lines = []
for i in range(17):
    grid_lines.append(Line((grid_x*i, 0), (grid_x*i, 1000), thickness=1))
    grid_lines.append(Line((0, grid_y * i), (10000, grid_y * i), thickness=1))

def draw_grid():
    for i in grid_lines:
        i.draw(screen)

def progess_page():
    global current_step, target_pos, wall_height
    ### Progress Page ###
    calculator = Calculator(GRAVITY, INITIAL_THETA)
    robot_pos = calculator.calculate_robot_pos(target_pos)
    calculator.initial_pos_x = robot_pos[1]
    field = Field(grid_x * 2, grid_y * 4 - 30, wall_height, 0, target_pos[1]/10)

    initial_velocity = calculator.calculate_initial_velocity(field=field)

    ball = Ball(grid_x * 4 + 36, grid_y * 9 + 20, 5, initial_velocity, theta=60)
    robot_rpm = calculator.velocity_to_rpm(initial_velocity, ROBOT_CONSTANT)
    robot_volt_uses = [
        calculator.rpm_to_volt(robot_rpm, MOTOR_CONSTANT_1),
        calculator.rpm_to_volt(robot_rpm, MOTOR_CONSTANT_2)
    ]

    resulting_pwm = round(robot_volt_uses[0], 1)
    resulting_rpm = round(robot_rpm)

    button_back_2 = ButtonText(grid_x * 1, grid_y * 13 + 30, "Back", FONT_BOLD, PRIMARY_COLOR_300,
                               background_color=BACKGROUND_COLOR,
                               color_active=BACKGROUND_COLOR_300, padding_x=50, padding_y=10, border_radius=20)
    button_next_2 = ButtonText(grid_x * 14 - 100, grid_y * 13 + 30, "Simulate", FONT_BOLD, BACKGROUND_COLOR,
                               PRIMARY_COLOR_300, background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10,
                               border_radius=20)

    rec_2_1 = Rectangle(grid_x * 10 - 100, grid_y * 4 + 10, grid_x * 5, grid_y * 3 + 30, "white", border_radius=30)
    rec_2_2 = Rectangle(grid_x * 10 - 100, grid_y * 8 + 10, grid_x * 5, grid_y * 3 + 30, "white", border_radius=30)

    text_pwm = Text(grid_x * 10 - 45, grid_y * 4 + 25, "PWM", FONT_BOLD, PRIMARY_COLOR_100)
    text_pwm_result = Text(grid_x * 10 - 45, grid_y * 4 + 90, f"{resulting_pwm} V", FONT_BOLD, PRIMARY_COLOR_100)
    rec_2_4 = Rectangle(grid_x * 10 - 75, grid_y * 4 + 70, grid_x * 4 + 30, grid_y * 2, PRIMARY_COLOR_100,
                        border_radius=30)
    rec_2_5 = Rectangle(grid_x * 10 - 75 + 4, grid_y * 4 + 70 + 4, grid_x * 4 + 30 - 8, grid_y * 2 - 8, "white",
                        border_radius=27)

    text_rpm = Text(grid_x * 10 - 45, grid_y * 8 + 25, "RPM", FONT_BOLD, PRIMARY_COLOR_100)
    text_rpm_result = Text(grid_x * 10 - 45, grid_y * 8 + 90, f"{resulting_rpm} RPM", FONT_BOLD, PRIMARY_COLOR_100)
    rec_2_6 = Rectangle(grid_x * 10 - 75, grid_y * 8 + 70, grid_x * 4 + 30, grid_y * 2, PRIMARY_COLOR_100,
                        border_radius=30)
    rec_2_7 = Rectangle(grid_x * 10 - 75 + 4, grid_y * 8 + 70 + 4, grid_x * 4 + 30 - 8, grid_y * 2 - 8, "white",
                        border_radius=27)

    rec_2_3 = Rectangle(grid_x * 4 - 100, grid_y * 3 + 40, grid_x * 5, grid_x * 5, "white", border_radius=30)

    robot_pos_x_in_px = robot_pos[0] * 324 / 80
    field_starting_pos = (grid_x * 4 - 63, grid_y * 3 + 85)
    field_ending_pos = (field_starting_pos[0] + robot_pos_x_in_px, field_starting_pos[1])

    dimension_top = DimensionLine((field_starting_pos[0], field_starting_pos[1] - 10),
                                  (field_ending_pos[0], field_ending_pos[1] - 10))
    sprite_field_top = Sprite(field_starting_pos[0], field_starting_pos[1], graphic_path / "field_top.png", scaling=0.145)
    sprite_robot_top = Sprite(field_ending_pos[0], field_starting_pos[1] + 3, graphic_path / "Topview.png", scaling=0.4)
    text_robot_pos_x = Text(field_starting_pos[0] + (field_ending_pos[0] - field_starting_pos[0]) / 2 - 33,
                            field_starting_pos[1] - 45, f"{round(robot_pos[0], 1)} cm", FONT_SMALL, PRIMARY_COLOR_100)

    progress_components = [button_back_2, button_next_2, rec_2_1, rec_2_2, rec_2_3, rec_2_4, rec_2_5, text_pwm,
                           text_pwm_result,
                           rec_2_6, rec_2_7, text_rpm, text_rpm_result, sprite_field_top, sprite_robot_top,
                           dimension_top, text_robot_pos_x]

    ### Simulate Page ###
    button_back_3 = ButtonText(grid_x * 1, grid_y * 13 + 30, "Back", FONT_BOLD, PRIMARY_COLOR_300,
                               background_color=BACKGROUND_COLOR,
                               color_active=BACKGROUND_COLOR_300, padding_x=50, padding_y=10, border_radius=20)
    button_next_3 = ButtonText(grid_x * 14 - 40, grid_y * 13 + 30, "END", FONT_BOLD, BACKGROUND_COLOR,
                               PRIMARY_COLOR_300,
                               background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10, border_radius=20)
    icon_button_replay = ButtonIcon(screen_width/2-20, grid_y * 13 + 30, graphic_path / "replay.png", .6)

    rec_3_1 = Rectangle(grid_x * 2, grid_y * 3 + 20, grid_x * 12, grid_x * 5, "white", border_radius=30)
    text_pwm_simulate = Text(grid_x * 2 + 45, grid_y * 3 + 40, f"PWM = {resulting_pwm} V", FONT_LIGHT_SMALL,
                             PRIMARY_COLOR_100)
    text_rpm_simulate = Text(grid_x * 2 + 45, grid_y * 3 + 40 + 25, f"RPM = {resulting_rpm} RPM", FONT_LIGHT_SMALL,
                             PRIMARY_COLOR_100)

    simulate_components = [icon_button_replay, button_next_3, button_back_3, rec_3_1, text_pwm_simulate, text_rpm_simulate, field]

    ball_time = 0
    while True:
        screen.fill(BACKGROUND_COLOR)
        progress_bar.draw(screen, status=current_step)
        if current_step == "progress":
            for component in progress_components:
                component.draw(screen)
        elif current_step == "simulate":
            ball.move(ball_time)
            ball_time += 0.008
            if ball.pos_y > (grid_x * 5 + grid_y * 3-11):
                ball_showing = False
            elif ball.pos_y < grid_x * 2:
                ball_showing = False
            else:
                ball_showing = True
            for component in simulate_components:
                component.draw(screen)
            print(ball_showing)
            if ball_showing:
                ball.draw(screen)

        for event in pg.event.get():
            if current_step == "progress":
                if button_next_2.handle_mouse_event(event):
                    current_step = "simulate"
                if button_back_2.handle_mouse_event(event):
                    current_step = "setup"
                    return

            elif current_step == "simulate":
                if button_next_3.handle_mouse_event(event):
                    current_step = "setup"
                    return
                if button_back_3.handle_mouse_event(event):
                    current_step = "progress"
                if icon_button_replay.handle_mouse_event(event):
                    ball_showing = True
                    ball_time = 0
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.flip()
        fpsClock.tick(fps)


### Input Page ###

button_next_i = ButtonText(grid_x * 14 - 40, grid_y * 13 + 30, "Done", FONT_BOLD, BACKGROUND_COLOR,
                           PRIMARY_COLOR_300,
                           background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10, border_radius=30)
i_div_1_starting = grid_x*9-50
i_div_1_width = grid_x*5+40

input_box_target_x = TextInputBox(i_div_1_starting, grid_y*5-45, grid_x*3-30, FONT_BOLD, color=PRIMARY_COLOR_100)
input_box_target_y = TextInputBox(i_div_1_starting, grid_y*7-20-45, grid_x*3-30, FONT_BOLD, color=PRIMARY_COLOR_100)
rect_i_1 = Rectangle(i_div_1_starting - grid_x, grid_y * 4+30-45, i_div_1_width, grid_y*4-30, "white", border_radius=30)

text_i_1 = Text(i_div_1_starting - 40, grid_y*5+5-45, f"X", FONT_BOLD, PRIMARY_COLOR_100)
text_i_2 = Text(i_div_1_starting + grid_x*2 + 60, grid_y*5+5-45, f"mm", FONT_BOLD, PRIMARY_COLOR_100)
text_i_3 = Text(i_div_1_starting - 40, grid_y*7-20+5-45, f"Y", FONT_BOLD, PRIMARY_COLOR_100)
text_i_4 = Text(i_div_1_starting + grid_x*2 + 60, grid_y*7-20+5-45, f"mm", FONT_BOLD, PRIMARY_COLOR_100)
text_i_5 = Text(i_div_1_starting - grid_x, grid_y*3+25-45, f"Input Target", FONT_BOLD, PRIMARY_COLOR_100)
text_i_warning = TextWarning(i_div_1_starting - grid_x + 40, grid_y*7+5, f"", FONT_WARNING, WARNING_COLOR)
button_add_target = ButtonText(i_div_1_starting + i_div_1_width-grid_x+25, grid_y*5+20-45, "+", FONT_BOLD_BIG,
                                             BACKGROUND_COLOR, background_color=PRIMARY_COLOR_100,
                                             color_active=PRIMARY_COLOR_300, padding_x=55, padding_y=0,
                                             border_radius=100)

rect_i_2 = Rectangle(grid_x*2-16, grid_y * 1+20, grid_x*4+60, grid_x*4+30-20, "white", border_radius=30)
sprite_topview_display = Sprite(grid_x*2+10, grid_y * 1+50-20, graphic_path / "bg_target_line.png", 0.3)
input_boxes = [input_box_target_x, input_box_target_y]
display_block_manager = DisplayBlockManager(100, grid_y*10+20, grid_x, grid_y)
input_components = [text_i_warning, rect_i_1, text_i_1, text_i_2, text_i_3, text_i_4, text_i_5, button_add_target, rect_i_2, sprite_topview_display, button_next_i, display_block_manager]

### Setup Page ###
selector = Selector(grid_x * 6 - 100, grid_y * 9-20 + 30)

icon_button_setting = ButtonIcon(grid_x-20, grid_y-10, graphic_path / "gear.png", .15)
target_pos = ("-", "-")
button_next_1 = ButtonText(grid_x * 14 - 100, grid_y * 13 + 30, "next →", FONT_BOLD, BACKGROUND_COLOR, PRIMARY_COLOR_300,
                           background_color=PRIMARY_COLOR_100, padding_x=50, padding_y=10, border_radius=20)
text_1_warning = TextWarning(grid_x * 13 - 100, grid_y * 13, f"", FONT_WARNING, WARNING_COLOR)

div_1_starting_x = grid_x * 8+20
text_1_1 = Text(grid_x * 3+10, grid_y * 3, "Select a Target", FONT_BOLD, PRIMARY_COLOR_100)
text_1_2 = Text(div_1_starting_x+20, grid_y * 4, "Selected Target position", FONT_BOLD, PRIMARY_COLOR_100)
text_1_3 = Text(div_1_starting_x+20, grid_y * 9, "Wall height", FONT_BOLD, PRIMARY_COLOR_100)

text_x_pos = Text(div_1_starting_x+30+30, grid_y * 5 + 15, f"X : {target_pos[0]} mm", FONT_BOLD, PRIMARY_COLOR_100)
text_y_pos = Text(div_1_starting_x+30+30, grid_y * 7 + 5, f"Y : {target_pos[1]} mm", FONT_BOLD, PRIMARY_COLOR_100)
rec_1_1 = Rectangle(div_1_starting_x+30, grid_y * 5 + 10, grid_x * 2+70, grid_y * 1+20, "white", border_radius=30)
rec_1_2 = Rectangle(div_1_starting_x+30, grid_y * 7, grid_x * 2+70, grid_y * 1+20, "white", border_radius=30)

wall_height = 50
rec_1_3 = Rectangle(div_1_starting_x+30, grid_y * 10+10, grid_x * 4-12, grid_y * 1+20, GRAY_COLOR, border_radius=30)

rec_button_select_poss = [div_1_starting_x+30, grid_x * 10+15+20]
button_wall_height_1 = ButtonText(rec_button_select_poss[0], grid_y * 10+11, "50 cm", FONT_BOLD, BACKGROUND_COLOR,
                               PRIMARY_COLOR_300, padding_x=50, padding_y=15,
                               border_radius=30)
button_wall_height_2 = ButtonText(rec_button_select_poss[1], grid_y * 10+11, "100 cm", FONT_BOLD, BACKGROUND_COLOR,
                               PRIMARY_COLOR_300, padding_x=50, padding_y=15,
                               border_radius=30)

rec_button_select = Rectangle(div_1_starting_x+30, grid_y * 10+10, grid_x * 2-10, grid_y * 1+20, PRIMARY_COLOR_100, border_radius=30)
setup_components = [text_1_warning, icon_button_setting, rec_1_1, rec_1_2, rec_1_3, text_x_pos, text_y_pos, text_1_1, text_1_2, text_1_3, selector, button_next_1]
buttons_wall_height = [button_wall_height_1, button_wall_height_2]

wanted_rec_button_select_pos = rec_button_select_poss[0]
while True:
    screen.fill(BACKGROUND_COLOR)
    if target_pos == ("-", "-"):
        button_next_1.set_color(GRAY_COLOR)
    if current_step != "input":
        progress_bar.draw(screen, status=current_step)
    if current_step == "setup":
        if rec_button_select.pos_x < wanted_rec_button_select_pos:
            rec_button_select.pos_x += ANIMATION_SPEED
            if rec_button_select.pos_x > wanted_rec_button_select_pos:
                rec_button_select.pos_x = wanted_rec_button_select_pos

        elif rec_button_select.pos_x > wanted_rec_button_select_pos:
            rec_button_select.pos_x -= ANIMATION_SPEED
            if rec_button_select.pos_x < wanted_rec_button_select_pos:
                rec_button_select.pos_x = wanted_rec_button_select_pos

        for component in setup_components:
            component.draw(screen)
        rec_button_select.draw(screen)

        for button in buttons_wall_height:
            button.draw(screen)
    elif current_step == "input":
        for component in input_components:
            component.draw(screen)
        for component in input_boxes:
            component.draw(screen)

    # draw_grid()

    event_list = pg.event.get()
    for component in input_boxes:  # input boxes event
        component.update(event_list)

    for event in event_list:

        if current_step == "input":
            display_block_manager.handle_event(event)
            if button_next_i.handle_mouse_event(event):
                current_step = "setup"
                display_block_manager.render_block()
                selector.render()
                text_i_warning.set_content("")
                time.sleep(.1)

            elif button_add_target.handle_mouse_event(event):
                if not input_box_target_x.text or not input_box_target_y.text:
                    text_i_warning.set_content("Your input box is Empty.")
                    text_i_warning.shake()
                elif not input_box_target_x.text.isdigit() or not input_box_target_y.text.isdigit():
                    text_i_warning.set_content("Invalid Number (mai dai amp pom rok =w=).")
                    text_i_warning.shake()
                elif int(input_box_target_y.text) > 300 or int(input_box_target_y.text) < 65:
                    text_i_warning.set_content("Invalid Target Position.")
                    text_i_warning.shake()
                elif int(input_box_target_x.text) > abs((int(input_box_target_y.text) - 300) / 2) or int(input_box_target_x.text) < -abs((int(input_box_target_y.text) - 300) / 2):
                    print(abs((int(input_box_target_y.text) - 300) / 2))
                    text_i_warning.set_content("Invalid Target Position.")
                    text_i_warning.shake()
                elif len(display_block_manager.display_blocks) >= 3:
                    text_i_warning.set_content("You can only have at most 3 Targets at once.")
                    text_i_warning.shake()
                else:
                    inputted_target_pos = [input_box_target_x.text, input_box_target_y.text]
                    display_block_manager.add_block(inputted_target_pos)
                    text_i_warning.set_content("")
        elif current_step == "setup":
            if button_next_1.handle_mouse_event(event):
                if target_pos != ("-", "-"):
                    current_step = "progress"
                    progess_page()
                    text_1_warning.set_content("")
                else:
                    text_1_warning.set_content("Please, Select a Target first.")
                    text_1_warning.shake()
            elif icon_button_setting.handle_mouse_event(event):
                current_step = "input"
            elif button_wall_height_1.handle_mouse_event(event):
                wall_height = 50
                rec_button_select.width = grid_x * 2 - 10
                wanted_rec_button_select_pos = rec_button_select_poss[0]

            elif button_wall_height_2.handle_mouse_event(event):
                wall_height = 100
                rec_button_select.width = grid_x * 2 + 2
                wanted_rec_button_select_pos = rec_button_select_poss[1]

            selector_event = selector.handle_mouse_event(event)
            if selector_event:
                target_pos = selector_event
                text_x_pos.set_content(f"X : {target_pos[0]} mm")
                text_y_pos.set_content(f"Y : {target_pos[1]} mm")

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.flip()
    fpsClock.tick(fps)
