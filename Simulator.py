class Simulator():

    def __init__(self, car, visualizer, total_time = 10, delta_t = 0.1):
        self.car = car
        self.visualizer = visualizer
        self.total_time = total_time
        self.delta_t = delta_t
    
    def simulate(self):
        for frame in range(int(self.total_time//self.delta_t)):
            print("frame = ", frame, "     " , "time = ", frame * self.delta_t)
            self.visualizer.visualize(self.car, frame)
            self.car.Drive(self.delta_t)