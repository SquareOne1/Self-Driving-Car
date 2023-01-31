import math
import numpy as np

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

        self.predictions = None

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def set_steering_rate(self, steering_rate):
        self.steering_rate = steering_rate
        
    def get_predictions(self):
        return self.predictions

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
    
    def get_velocity(self):
        return self.velocity
    
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
        self.psi = self.psi + delta_t * self.steering_rate
        self.velocity = self.velocity + self.acceleration * delta_t
    
    def predict_states(self, flat_control_signal):
        curr_x = self.get_x()
        curr_y = self.get_y()
        curr_theta = self.get_theta()
        curr_psi = self.get_psi()
        curr_velocity = self.get_velocity()

        predictions = []

        for i in range(self.look_ahead_steps):
            acceleration = flat_control_signal[i]
            steering_rate = flat_control_signal[self.look_ahead_steps + i]
            
            next_x = curr_x + self.delta_t * curr_velocity * math.cos(curr_theta + curr_psi)
            next_y = curr_y + self.delta_t * curr_velocity * math.sin(curr_theta + curr_psi)
            next_theta = curr_theta + self.delta_t * curr_velocity/(self.car.get_length()) * math.sin(curr_psi)
            next_psi = curr_psi + self.delta_t * steering_rate
            next_velocity = curr_velocity + acceleration * self.delta_t

            predictions.append([next_x, next_y, next_theta, next_psi, next_velocity])

            curr_x = next_x
            curr_y = next_y
            curr_theta = next_theta
            curr_psi = next_psi
            curr_velocity = next_velocity

        self.predictions = predictions
        return np.array(predictions)

    def Drive(self, delta_t):
        self.update_states(delta_t)
        self.save_history()

    def PrintCarStates(self):
        print("x = ", self.x)
        print("y = ", self.y)
        print("theta = ", self.theta)
        print("psi = ", self.psi)
        print("velocity = ", self.velocity)