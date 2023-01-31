class PointSelector:
    def __init__(self, car, trajectory, look_ahead_steps):
        self.car = car
        self.trajectory = trajectory
        self.look_ahead_steps = look_ahead_steps
        self.selected_points = []
    
    def get_selected_points(self):
        return self.selected_points

    def find_closest_point_index(self):
        waypoints = self.trajectory.get_waypoints()
        min_distance = float("+inf")
        min_index = 0

        for i in range(len(waypoints)):
            distance = (self.car.get_x() - waypoints[i,0]) ** 2 + (self.car.get_y() - waypoints[i,1]) ** 2
            if distance < min_distance:
                min_distance = distance
                min_index = i

        return min_index
    
    def select_points(self):
        min_index = self.find_closest_point_index()
        print(min_index)
        selected_waypoints = []
        for i in range(min_index + 1, min_index + self.look_ahead_steps + 1):
            selected_waypoints.append(self.trajectory.get_waypoints()[i % len(self.trajectory.get_waypoints())])

        self.selected_points = selected_waypoints