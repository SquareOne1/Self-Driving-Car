from Car import Car
from Simulator import Simulator
import math
from Visualization import Visualizer
from Trajectory import Trajectory

save_frames_path = "C:/Users/arals/Desktop/SquareOne/figs"
save_video_path = "C:/Users/arals/Desktop/SquareOne/figs"


car = Car(0, 0, 0, math.pi/6, 2, 2.057, 2.665)
trajectory = Trajectory(0.05)

simulator = Simulator(car, trajectory , save_frames_path, save_video_path, 20, 0.1)
simulator.simulate()
simulator.convert_to_mp4()