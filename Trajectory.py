import numpy as np
import math

class Trajectory:
    def __init__(self, delta_t):
        self.waypoints = None
        self.delta_t = delta_t
        self.waypoints_x = []
        self.waypoints_y = []
        self.compute_waypoints()

    def get_waypoints(self):
        return self.waypoints
    
    def get_waypoints_x(self):
        return self.waypoints_x
    
    def get_waypoints_y(self):
        return self.waypoints_y

    def compute_waypoints(self, radius = 8):
        timestamps = np.arange(0, 2 * math.pi, self.delta_t)
        waypoints = []

        for t in timestamps:
            x = radius * math.cos(2 * math.pi * t)
            y =  radius * math.sin(2 * math.pi * t)

            self.waypoints_x.append(x)
            self.waypoints_y.append(y)
            waypoints.append([x, y])
        
        self.waypoints = np.array(waypoints)


trajectory = Trajectory(0.1)
