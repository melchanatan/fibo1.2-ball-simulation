class RigidBody :
    def __init__(self):
        pass

    def check_collison(self ,ball , collisoned):
        if ( collisoned.pos_x - collisoned.width/2 <= ball.pos_x + ball.radius <= collisoned.pos_x + collisoned.width/2  and collisoned.pos_y - collisoned.height/2 <= ball.pos_y + ball.radius <= ball.pos_x + ball.radius <= collisoned.pos_y + collisoned.height/2):
            return True
        else :
            return False