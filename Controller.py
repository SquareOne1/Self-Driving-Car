from scipy.optimize import minimize
import numpy as np
from Car import Car
import math

class MPC:
    def __init__(self, car, point_selector, look_ahead_steps, desired_speed, delta_t):
        self.car = car
        self.point_selector = point_selector
        self.look_ahead_steps = look_ahead_steps
        self.desired_speed = desired_speed
        self.delta_t = delta_t

        self.optimal_control_signal = np.zeros((2, look_ahead_steps))
        
        self.min_acceleration = -2.0
        self.max_acceleration = 2.0
        self.min_steering_rate = -1.0
        self.max_steering_rate = 1.0
        self.predictions = None
        self.optimization_bounds = None

        self.compute_optimization_bounds()
    
    def predict_states(self, flat_control_signal):
        curr_x = self.car.get_x()
        curr_y = self.car.get_y()
        curr_theta = self.car.get_theta()
        curr_psi = self.car.get_psi()
        curr_velocity = self.car.get_velocity()

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
    
    def get_predictions(self):
        return self.predictions
    
    def generate_acceleration_bounds(self):
        acceleration_bounds = []
        for i in range(self.look_ahead_steps):
            acceleration_bounds.append((self.min_acceleration, self.max_acceleration))
        
        return acceleration_bounds
        
    def generate_steering_rate_bounds(self):
        steering_rate_bounds = []

        for i in range(self.look_ahead_steps):
            steering_rate_bounds.append((self.min_steering_rate, self.max_steering_rate))
        
        return steering_rate_bounds
    
    def compute_optimization_bounds(self):
        acceleration_bounds = self.generate_acceleration_bounds()
        steering_rate_bounds = self.generate_steering_rate_bounds()
        self.optimization_bounds = tuple(acceleration_bounds + steering_rate_bounds)

    def compute_steering_rate_smoothness_cost(self, control_signal):
        steering_rate_smoothness_cost = 0
        for i in range(self.look_ahead_steps, len(control_signal) - 1):
            steering_rate_smoothness_cost += (control_signal[i + 1] - control_signal[i]) ** 2
        
        return steering_rate_smoothness_cost

    def compute_acceleration_smoothness_cost(self, control_signal):
        acceleration_smoothness_cost = 0
        for i in range(self.look_ahead_steps - 1):
            acceleration_smoothness_cost += (control_signal[i + 1] - control_signal[i]) ** 2
        
        return acceleration_smoothness_cost

    def total_cost(self, flat_control_signal):
        predictions = self.predict_states(flat_control_signal)
        cost = self.compute_velocity_cost(predictions) + \
               30 * self.compute_tracking_cost(predictions) + \
               10 * self.compute_acceleration_smoothness_cost(flat_control_signal) + \
               10 * self.compute_steering_rate_smoothness_cost(flat_control_signal)

        return cost

    def compute_tracking_cost(self, predictions):
        tracking_cost = 0
        selected_points = self.point_selector.get_selected_points()
        for pred, point in zip(predictions, selected_points):
            tracking_cost += (point[0] - pred[0]) ** 2 + (point[1] - pred[1]) ** 2
        
        return tracking_cost

    def compute_velocity_cost(self, predictions):
        velocity_cost = 0
        for pred in predictions:
            velocity_cost += (self.desired_speed - pred[4]) ** 2
        
        return velocity_cost

    def minimize_cost_function(self):
        initial_guess = np.zeros(2 * self.look_ahead_steps)
        print(self.optimization_bounds)
        result = minimize(self.total_cost, initial_guess, bounds=self.optimization_bounds)
        print("Optimization is Done!!!")
        print(result.x)
        self.optimal_control_signal = result.x

    def send_control_signal_to_car(self):
        self.car.set_acceleration(self.optimal_control_signal[0])
        self.car.set_steering_rate(self.optimal_control_signal[self.look_ahead_steps + 1])

    def execute(self):
        self.point_selector.select_points()
        self.minimize_cost_function()
        self.predict_states(self.optimal_control_signal)
        self.send_control_signal_to_car()

'''
car = Car(0, 0, 0, math.pi/6, 0, 2.057, 2.665)
controller = MPC(car, look_ahead_steps = 5, desired_speed = 2, delta_t = 0.01)
print(controller.minimize_cost_function())
'''