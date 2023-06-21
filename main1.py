import math

class Calculator:
    def __init__(self, gravity=0, initial_theta=0, initial_pos_y=0):
        self.__gravity = gravity
        self.initial_pos_y = initial_pos_y
        self.initial_theta = initial_theta

    def calculate_initial_velocity(self, y):
        radian = (self.initial_theta * 2 / 180) * math.pi
        return ((self.__gravity * (self.initial_pos_y+2+y/100+0.13125)) / math.sin(radian)) ** (1 / 2)

    def velocity_to_rpm(self, initial_velocity, k):
        return ((1000 * initial_velocity) / math.pi) * k

    def rpm_to_volt(self, rpm, motor_constant):
        return 0.0072 * (rpm + motor_constant)


calculator = Calculator(9.81, 60, .21)
k1 = 188.57
k1 = 170.88

velocity = 0.051
rpm = calculator.velocity_to_rpm(velocity, 1)
volt = calculator.rpm_to_volt(rpm, 0)

print(velocity, rpm, volt)



k2 = 2359 / 1563.9991
print(k2)
# k1 = 1.508312888415345

velocity = calculator.calculate_initial_velocity(0)
rpm = calculator.velocity_to_rpm(velocity, k2)
volt = calculator.rpm_to_volt(rpm, k1)
print(velocity, rpm, volt)

k3 = 185.45
rpm = calculator.velocity_to_rpm(velocity, k2)
volt = calculator.rpm_to_volt(rpm, k3)
print(velocity, rpm, volt)
