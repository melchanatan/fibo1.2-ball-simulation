import math


class Calculator:
    def __init__(self, gravity=0, initial_theta=0, initial_pos_x=0):
        self.__gravity = gravity
        self.initial_pos_x = initial_pos_x
        self.initial_theta = initial_theta

    def calculate_initial_velocity(self, field):
        radian = (self.initial_theta * 2 / 180) * math.pi
        return ((self.__gravity * self.initial_pos_x) / math.sin(radian)) ** (1 / 2)

    def velocity_to_rpm(self, initial_velocity, robot_constant):
        return (1000 * initial_velocity) / math.pi

    def rpm_to_volt(self, rpm, motor_constant):
        return rpm * 12 / 1666.67

    def calculate_robot_pos(self, target_pos):
        return target_pos[0] - 20, 0
