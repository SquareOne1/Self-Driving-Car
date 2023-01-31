import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patches

class Visualizer:
    def __init__(self, frames_save_path):
        self.frames_save_path = frames_save_path
        self.figure = plt.figure()
        self.axs = self.figure.gca()

    def DrawRectangle(self, center_x, center_y, width, hight, rotation, facecolor = "blue", edgecolor = "black"):
        t_start = self.axs.transData
        rectangle = patches.Rectangle((center_x - width/2.0, center_y - hight/2.0), 
                                    width, 
                                    hight, 
                                    facecolor = facecolor ,
                                    edgecolor = edgecolor)

        t = mpl.transforms.Affine2D().rotate_around(center_x, center_y, rotation)
        t_end = t + t_start
        rectangle.set_transform(t_end)
        self.axs.add_patch(rectangle)

    def DrawTheCarBody(self, car):
        self.DrawRectangle(car.get_x(), car.get_y(), car.get_length(), car.get_width(), car.get_theta(), facecolor = "#89ABE3FF")
    

    def DrawCarCenter(self, car):
        self.axs.plot([car.get_x()], [car.get_y()], 'r',marker='.', markersize = 5)

    def DrawFrontWheels(self, car):
        t_start = self.axs.transData
        right_wheel = patches.Rectangle((car.get_x() + car.get_length()/2.0 - car.get_wheel_diameter()/2.0, 
                                        car.get_y() - car.get_width()/2.0 - car.get_wheel_width()/2.0), 
                                        car.get_wheel_diameter(),
                                        car.get_wheel_width() , 
                                        facecolor = "red" , 
                                        edgecolor = "black")

        left_wheel = patches.Rectangle((car.get_x() + car.get_length()/2.0 - car.get_wheel_diameter()/2.0,
                                        car.get_y() + car.get_width()/2.0 - car.get_wheel_width()/2.0), 
                                        car.get_wheel_diameter(), 
                                        car.get_wheel_width() , 
                                        facecolor = "red" , 
                                        edgecolor = "black")

        t_right = mpl.transforms.Affine2D().rotate_around(car.get_x() + car.get_length()/2.0, car.get_y() - car.get_width()/2.0, car.get_psi())
        t_left = mpl.transforms.Affine2D().rotate_around(car.get_x() + car.get_length()/2.0, car.get_y() + car.get_width()/2.0, car.get_psi())
        t = mpl.transforms.Affine2D().rotate_around(car.get_x(), car.get_y(), car.get_theta())
        t_right_end = t_right + t + t_start
        t_left_end =  t_left + t + t_start
        right_wheel.set_transform(t_right_end)
        left_wheel.set_transform(t_left_end)
        self.axs.add_patch(right_wheel)
        self.axs.add_patch(left_wheel)

    def DrawBackWheels(self, car):
        t_start = self.axs.transData
        right_wheel = patches.Rectangle((car.get_x() - car.get_length()/2.0 - car.get_wheel_diameter()/2.0,
                                        car.get_y() - car.get_width()/2.0 - car.get_wheel_width()/2.0), 
                                        car.get_wheel_diameter(), 
                                        car.get_wheel_width(),
                                        facecolor = "red" ,
                                        edgecolor = "black")

        left_wheel = patches.Rectangle((car.get_x() - car.get_length()/2.0 - car.get_wheel_diameter()/2.0,
                                        car.get_y() + car.get_width()/2.0 + - car.get_wheel_width()/2.0),
                                        car.get_wheel_diameter(), car.get_wheel_width(),
                                        facecolor = "red",
                                        edgecolor = "black")
                                        
        t = mpl.transforms.Affine2D().rotate_around(car.get_x(), car.get_y(), car.get_theta())
        t_end = t + t_start
        right_wheel.set_transform(t_end)
        left_wheel.set_transform(t_end)
        self.axs.add_patch(right_wheel)
        self.axs.add_patch(left_wheel)

    def DrawCarTrajectory(self, car):
        self.axs.plot(car.get_x_history(), car.get_y_history(), color = '#3A6B35')

    def DrawTheWheels(self, car):
        self.DrawFrontWheels(car)
        self.DrawBackWheels(car)

    def SaveFig(self, frame):
        fig_name = "frame-" + "{:04n}".format(frame) + ".jpg"
        fig_path = self.frames_save_path + "/" + fig_name
        self.figure.savefig(fig_path)
        

    def SetFigureLimits(self):
        self.axs.set_xlim([-12, 12])
        self.axs.set_ylim([-12, 12])
        self.axs.set_aspect('equal', adjustable='box')
    
    def FetchCurrentActiveAxis(self):
        self.axs = self.figure.gca()

    def ClearCurrentActiveAxis(self):
        self.axs.cla()
    
    def DrawTrajectory(self, trajectory):
        self.axs.plot(trajectory.get_waypoints_x(), trajectory.get_waypoints_y())
    
    def DrawPredictions(self, controller):

        predictions = controller.get_predictions()
        if predictions:
            x = [pred[0] for pred in predictions]
            y = [pred[1] for pred in predictions]
            self.axs.plot(x, y, "r--")
    
    def DrawSelectedPoints(self, point_selector):

        selected_points = point_selector.get_selected_points()
        x = [pred[0] for pred in selected_points]
        y = [pred[1] for pred in selected_points]
        self.axs.plot(x, y, "r*")

    def visualize(self, car, trajectory, controller,point_selector, frame):
        self.DrawTheCarBody(car)
        self.DrawCarCenter(car)
        self.DrawTheWheels(car)
        self.DrawPredictions(controller)
        self.DrawTrajectory(trajectory)
        self.DrawSelectedPoints(point_selector)
        self.DrawCarTrajectory(car)
        self.SetFigureLimits()
        self.SaveFig(frame)
        self.ClearCurrentActiveAxis()