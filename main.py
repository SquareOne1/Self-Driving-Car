from Car import Car
from Simulator import Simulator
import math
from Trajectory import Trajectory
from Controller import MPC
from PointSelector import PointSelector
save_frames_path = "C:/Users/arals/Desktop/SquareOne/figs"
save_video_path = "C:/Users/arals/Desktop/SquareOne/figs"

look_ahead_steps = 5
desired_speed = 2
delta_t = 0.1
total_time = 40
car = Car(0, -4, 0, 0, 0, 2.057, 2.665)
trajectory = Trajectory(delta_t)
point_selector = PointSelector(car,trajectory, look_ahead_steps)
controller = MPC(car, point_selector, look_ahead_steps, desired_speed, delta_t)

simulator = Simulator(car, 
                      trajectory, 
                      controller, 
                      point_selector , 
                      save_frames_path, 
                      save_video_path, 
                      total_time, 
                      delta_t)

simulator.simulate()
#simulator.convert_to_mp4()