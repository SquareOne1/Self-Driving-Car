import math

class Car:
    def __init__(self, x, y, theta, psi, velocity, width, length):
        self.x = x
        self.y = y
        self.theta = theta
        self.psi = psi
        self.velocity = velocity
        self.width = width
        self.length = length

        self.wheel_diameter = 0.66294
        self.wheel_width = 0.25908

        self.steering_rate = 0
        self.acceleration = 0
        self.x_history = [self.x]
        self.y_history = [self.y]
    
    def get_x(self):
        return self.x
    
    def get_x_history(self):
        return self.x_history

    def get_y(self):
        return self.y
    
    def get_y_history(self):
        return self.y_history
    
    def get_theta(self):
        return self.theta
    
    def get_psi(self):
        return self.psi
    
    def get_length(self):
        return self.length
    
    def get_width(self):
        return self.width
    
    def get_wheel_diameter(self):
        return self.wheel_diameter
    
    def get_wheel_width(self):
        return self.wheel_width
    
    def set_steering_rate(self, streering_rate):
        self.steering_rate = streering_rate
    
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def save_history(self):
        self.x_history.append(self.x)
        self.y_history.append(self.y)

    def update_states(self, delta_t):
        self.x = self.x + delta_t * self.velocity * math.cos(self.theta + self.psi)
        self.y = self.y + delta_t * self.velocity * math.sin(self.theta + self.psi)
        self.theta = self.theta + delta_t * self.velocity/(self.length) * math.sin(self.psi)
        self.psi = self.psi + delta_t* self.steering_rate
        self.velocity = self.velocity + self.acceleration * delta_t
    
    def Drive(self, delta_t):
        self.update_states(delta_t)
        self.save_history()

    def PrintCarStates(self):
        print("x = ", self.x)
        print("y = ", self.y)
        print("theta = ", self.theta)
        print("psi = ", self.psi)
        print("velocity = ", self.velocity)