import pygame as pg
pg.init()

win_x, win_y = 1920, 1080
screen = pg.display.set_mode((win_x, win_y))

startX_pb = 960
startY_pb = 100
distance = 200
circle_size = 32

screen.fill((239, 247, 255))
font_text = pg.font.Font('freesansbold.ttf', 20)
font_num = pg.font.Font('freesansbold.ttf', 30)

COLOR_NAVY = pg.Color((33, 50, 94))
COLOR_SKYBLUE = pg.Color((189, 216, 241))
COLOR_GREEN = pg.Color((26, 95, 122))
COLOR_SKYBLUE_BG = pg.Color((239, 247, 255))

class progress_bar:
    def __init__(self, status=''):
        self.status = status

    def show(self, screen, status):
        self.status = status
        self.color_num1 = pg.Color('white')
        self.color_num2 = COLOR_NAVY
        self.color_num3 = COLOR_NAVY
        self.num2 = '2'

        if (self.status == 'upload'):
            self.color1 = COLOR_NAVY
            self.color2 = COLOR_SKYBLUE
            self.color3 = COLOR_SKYBLUE
            self.num = '1'

        elif (self.status == 'progress'):
            self.color1 = COLOR_GREEN
            self.color2 = COLOR_NAVY
            self.color3 = COLOR_SKYBLUE
            self.color_num2 = pg.Color('white')
            self.num = u'\N{check mark}'

        elif (self.status == 'simulate'):
            self.color1 = COLOR_GREEN
            self.color2 = COLOR_GREEN
            self.color3 = COLOR_NAVY
            self.color_num2 = pg.Color('white')
            self.color_num3 = pg.Color('white')
            self.num = u'\u2713'
            self.num2 = u'\u2713'

        pg.draw.circle(screen,self.color1,(startX_pb-distance, startY_pb), circle_size)
        pg.draw.circle(screen,self.color2,(startX_pb, startY_pb),circle_size)
        pg.draw.circle(screen,self.color3,(startX_pb+distance, startY_pb),circle_size)
        pg.draw.rect(screen, self.color2,(startX_pb-(distance-circle_size), startY_pb, distance-circle_size/2+circle_size, 5))
        pg.draw.rect(screen, self.color3,(startX_pb+circle_size, startY_pb, distance-2*circle_size, 5))

        text = font_text.render('upload', True, self.color1, COLOR_SKYBLUE_BG)
        textRect = text.get_rect()
        textRect.center = (startX_pb-distance, startY_pb+50)
        screen.blit(text, textRect)

        text2 = font_text.render('progress', True, self.color2, COLOR_SKYBLUE_BG)
        text2Rect = text2.get_rect()
        text2Rect.center = (startX_pb, startY_pb+50)
        screen.blit(text2, text2Rect)

        text3 = font_text.render('simulate', True, self.color3, COLOR_SKYBLUE_BG)
        text3Rect = text3.get_rect()
        text3Rect.center = (startX_pb+distance, startY_pb+50)
        screen.blit(text3, text3Rect)

        num = font_num.render(self.num, True, self.color_num1, self.color1)
        numRect = num.get_rect()
        numRect.center = (startX_pb-distance, startY_pb)
        screen.blit(num, numRect)

        num2 = font_num.render(self.num2, True, self.color_num2, self.color2)
        num2Rect = num2.get_rect()
        num2Rect.center = (startX_pb, startY_pb)
        screen.blit(num2, num2Rect)

        num3 = font_num.render('3', True, self.color_num3, self.color3)
        num3Rect = num3.get_rect()
        num3Rect.center = (startX_pb+distance, startY_pb)
        screen.blit(num3, num3Rect)


while(1):
    progress_bar().show(screen, 'progress')

    pg.time.delay(1)
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
