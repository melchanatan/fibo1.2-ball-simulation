import pygame as pg
import math
pg.init()

class Ball :
    def __init__(self ,pos_x=50, pos_y=300, radius=4 , initial_velocity=20 ,theta=60 ,gravity=-2 ,last_pos_x=0 ,last_pos_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.initial_velocity = initial_velocity
        self.theta = theta
        self.gravity = gravity
        self.last_pos_x = last_pos_x
        self.last_pos_y = last_pos_y

    def move(self , time) :
        radian = (self.theta/180)*math.pi
        Ux = self.initial_velocity*(math.cos(radian))
        Uy = self.initial_velocity*(math.sin(radian))
        Sy = Uy*(time) + 0.5*self.gravity*(time**2)
        Sx = Ux*(time)

        self.pos_x += Sx - self.last_pos_x
        self.last_pos_x = Sx
        self.pos_y -= Sy - self.last_pos_y
        self.last_pos_y = Sy

    def draw(self):
        pg.draw.circle(screen,(255,0,0),(self.pos_x,self.pos_y),self.radius)

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path, scaling=1):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scaling = scaling

        self.default_image = pg.image.load(image_path).convert_alpha()
        self.width = self.default_image.get_rect().width
        self.height = self.default_image.get_rect().height
        self.image = pg.transform.scale(self.default_image, (self.width*self.scaling, self.height*self.scaling))
        self._rect = self.image.get_rect()

    def draw(self, screen):
        self._rect.topleft = (self.pos_x, self.pos_y)
        screen.blit(self.image, self._rect)

    def scale_image(self, scale):
        self.height = self.default_image.get_rect().height
        self.width = self.default_image.get_rect().width

        self.image = pg.transform.scale(self.default_image, (self.width * scale, self.height * scale))

class RigidBody(Sprite) : 
    def __init__(self, *args):
        super().__init__(*args)

    def check_collison(self ,ball):
        if ( self.pos_x - self.width/2 <= ball.pos_x + ball.radius <= self.pos_x + self.width/2  and self.pos_y - self.height/2 <= ball.pos_y + ball.radius <= self.pos_y + self.height/2):
            return True
        else :
            return False


win_x , win_y = 800 , 480
screen = pg.display.set_mode((win_x,win_y))
posX , posY = 100 , win_y*6/7
time = 0
ball = Ball()
pic = RigidBody(200,300,"C:/Users/theet/Desktop/backgroud/99415552_p0_master1200.jpg",0.2)
collidable_components = [pic]
while(1):
    if pic.check_collison(ball) == True :
        screen.fill((255, 255, 255))
    if pic.check_collison(ball) == False :
        screen.fill((255, 0, 0))
    pic.draw(screen)
    ball.move(time)

    ball.draw()
    time += 0.1
    

    pg.time.delay(1)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()