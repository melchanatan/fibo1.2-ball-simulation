import math


class Ball:
    def __init__(self, pos_x, pos_y, radius, initial_velocity, theta, gravity=9.81, last_pos_x=0, last_pos_y=0):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__radius = radius
        self.initial_velocity = initial_velocity
        self.theta = theta
        self.gravity = gravity
        self.last_pos_x = last_pos_x
        self.last_pos_y = last_pos_y

    def move(self, time):
        radian = (self.theta / 180) * math.pi
        Ux = self.initial_velocity * (math.cos(radian))
        Uy = self.initial_velocity * (math.sin(radian))
        Sy = Uy * time + 0.5 * self.gravity * (time ** 2)
        Sx = Ux * time

        self.__pos_x += Sx - self.last_pos_x
        self.last_pos_x = Sx
        self.__pos_y += Sy - self.last_pos_y
        self.last_pos_y = Sy
