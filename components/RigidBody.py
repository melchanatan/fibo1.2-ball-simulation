from components.Sprite import Sprite
from components.Ball import Ball

class RigidBody(Sprite) : 
    def __init__(self, *args):
        super().__init__(*args)

    def check_collison(self ,Ball):
        if ( self.pos_x <= Ball.pos_x + Ball.radius <= self.pos_x + (self.width*self.scaling) and self.pos_y <= Ball.pos_y + Ball.radius <= self.pos_y + (self.height*self.scaling)):
            return True
        else :
            return False