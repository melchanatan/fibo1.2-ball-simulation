import pygame as pg

distance = 160
circle_size = 22

COLOR_NAVY = pg.Color((33, 50, 94))
COLOR_SKYBLUE = pg.Color((189, 216, 241))
COLOR_GREEN = pg.Color((26, 95, 122))
COLOR_SKYBLUE_BG = pg.Color((239, 247, 255))

class ProgressBar:
    def __init__(self, starting_x, starting_y, font_text, font_number, status=''):
        self.status = status
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.font_text = font_text
        self.font_number = font_number


    def draw(self, screen, status):
        self.status = status
        self.color_num1 = pg.Color('white')
        self.color_num2 = COLOR_NAVY
        self.color_num3 = COLOR_NAVY
        self.num2 = '2'

        if (self.status == 'setup'):
            self.color1 = COLOR_NAVY
            self.color2 = COLOR_SKYBLUE
            self.color3 = COLOR_SKYBLUE
            self.num = '1'

        elif (self.status == 'progress'):
            self.color1 = COLOR_GREEN
            self.color2 = COLOR_NAVY
            self.color3 = COLOR_SKYBLUE
            self.color_num2 = pg.Color('white')
            self.num = '✔'

        elif (self.status == 'simulate'):
            self.color1 = COLOR_GREEN
            self.color2 = COLOR_GREEN
            self.color3 = COLOR_NAVY
            self.color_num2 = pg.Color('white')
            self.color_num3 = pg.Color('white')
            self.num = "✔"
            self.num2 = "✔"

        pg.draw.circle(screen,self.color1,(self.starting_x-distance, self.starting_y), circle_size)
        pg.draw.circle(screen,self.color2,(self.starting_x, self.starting_y),circle_size)
        pg.draw.circle(screen,self.color3,(self.starting_x+distance, self.starting_y),circle_size)
        pg.draw.rect(screen, self.color2,(self.starting_x-(distance-circle_size), self.starting_y, distance-circle_size/2+circle_size, 5))
        pg.draw.rect(screen, self.color3,(self.starting_x+circle_size, self.starting_y, distance-2*circle_size, 5))

        text = self.font_text.render('upload', True, self.color1, COLOR_SKYBLUE_BG)
        textRect = text.get_rect()
        textRect.center = (self.starting_x-distance, self.starting_y+40)
        screen.blit(text, textRect)

        text2 = self.font_text.render('progress', True, self.color2, COLOR_SKYBLUE_BG)
        text2Rect = text2.get_rect()
        text2Rect.center = (self.starting_x, self.starting_y+40)
        screen.blit(text2, text2Rect)

        text3 = self.font_text.render('simulate', True, self.color3, COLOR_SKYBLUE_BG)
        text3Rect = text3.get_rect()
        text3Rect.center = (self.starting_x+distance, self.starting_y+40)
        screen.blit(text3, text3Rect)

        num = self.font_number.render(self.num, True, self.color_num1, self.color1)
        numRect = num.get_rect()
        numRect.center = (self.starting_x-distance, self.starting_y)
        screen.blit(num, numRect)

        num2 = self.font_number.render(self.num2, True, self.color_num2, self.color2)
        num2Rect = num2.get_rect()
        num2Rect.center = (self.starting_x, self.starting_y)
        screen.blit(num2, num2Rect)

        num3 = self.font_number.render('3', True, self.color_num3, self.color3)
        num3Rect = num3.get_rect()
        num3Rect.center = (self.starting_x+distance, self.starting_y)
        screen.blit(num3, num3Rect)
