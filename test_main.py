import pygame as pg
import math
pg.init()

from components.Field import Field
from components.Ball import Ball

win_x , win_y = 960 , 400
screen = pg.display.set_mode((win_x,win_y))
posX , posY = 100 , win_y*6/7
time = 0
ball = Ball(200,278,5.5,5,60,-9.81)
field = Field(0,0,100,0,3,1)


# def Info():
#     font = pg.font.Font(None, 20)
#     textSY = font.render('ball_x : ' + str(ball.pos_x) + ' ',True,(0,0,0))
#     textVX = font.render('ball_y : ' + str(ball.pos_y) + ' ',True,(0,0,0))
#     textpicx = font.render('pic_x : ' + str(pic.pos_x) + ' - ' + str(pic.pos_x + (pic.width*0.2)),True,(0,0,0))
#     textpicy = font.render('pic_y : ' + str(pic.pos_y) + ' - ' + str(pic.pos_y + (pic.height*0.2)),True,(0,0,0))
#     screen.blit(textSY,(10,60))
#     screen.blit(textVX,(10,80))
#     screen.blit(textpicx,(10,100))
#     screen.blit(textpicy,(10,120))


while(1):
    screen.fill((255, 255, 255))

    ball.move(time)
    field.draw(screen)
    ball.draw(screen)
    time += 0.001

    if ball.pos_y + ball.radius >= win_y - field.floor.height :
        pg.quit()
        exit()

    pg.time.delay(1)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()