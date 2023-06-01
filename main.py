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

# Initialize Pygame (always on top)
pg.init()

# Initial Variable
BACKGROUND_COLOR = (203, 178, 121)
FONT = pg.font.Font("freesansbold.ttf", 32)

fps = 60
fpsClock = pg.time.Clock()
pk = 2
screen_width, screen_height = 1366, 768

screen = pg.display.set_mode((screen_width, screen_height))

rec = Rectangle(2, 30, 40, 40)
tex = Text(screen_width // 2, screen_height // 2, "ehlo", FONT, text_color=(9, 1, 1),
           background_color=(100, 10, 100))
but = ButtonText(screen_width // 2 + 100, screen_height // 2 + 100, "ehlo", FONT, color_active=(1, 2, 3),
                 text_color=(9, 1, 1), background_color=(0, 0, 255), border_radius=10)
spr = Sprite(10, 19, os.path.join(".", "graphics", "button.png"), .1)
ibut = ButtonIcon(100, 190, "./graphics/button.png", .1)
lin = DimensionLine((100, 100), (100, 200), (1, 2, 1), 3)
fil = FileHandler(100, 100, 100 ,100)
# Game loop.
while True:
    screen.fill(BACKGROUND_COLOR)

    rec.draw(screen)
    tex.draw(screen)
    but.draw(screen)
    spr.draw(screen)
    ibut.draw(screen)
    lin.draw(screen)
    for event in pg.event.get():
        but.handle_mouse_event(event)
        ibut.handle_mouse_event(event)

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Update.

    # Draw.

    pg.display.flip()
    fpsClock.tick(fps)