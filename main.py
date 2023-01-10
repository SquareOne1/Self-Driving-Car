from Car import Car
from Simulator import Simulator
import math
from Visualization import Visualizer

save_frames_path = "C:/Users/arals/Desktop/SquareOne/Self-Driving-Car/figs"
car = Car(0, 0, 0, math.pi/6, 2, 2.057, 2.665)
visualizer = Visualizer(save_frames_path)

simulator = Simulator(car, visualizer, 20, 0.1)
simulator.simulate()