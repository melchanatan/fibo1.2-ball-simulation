import math


class Calculator:
    def __init__(self, gravity=0, initial_theta=0, initial_pos_y=0):
        self.__gravity = gravity
        self.initial_pos_y = initial_pos_y
        self.initial_theta = initial_theta

    def calculate_initial_velocity(self, field):
        radian = (self.initial_theta * 2 / 180) * math.pi
        return ((self.__gravity * (self.initial_pos_y+2+field.target/100+0.13125)) / math.sin(radian)) ** (1 / 2)

    def velocity_to_rpm(self, initial_velocity, robot_constant):
        return (1000 * initial_velocity) / math.pi

    def rpm_to_volt(self, rpm, motor_constant):
        return rpm * 12 / 1666.67

    def calculate_robot_pos(self, target_pos):
        return 40 + (target_pos[0]/10) - 10 , 0
