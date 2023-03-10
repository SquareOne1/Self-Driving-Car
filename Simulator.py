import os
import Visualization as vis

class Simulator():

    def __init__(self, car, trajectory,save_frames_path, save_video_path, total_time = 10, delta_t = 0.1):
        self.car = car
        self.save_frames_path = save_frames_path
        self.save_video_path = save_video_path
        self.image_format = "jpg"
        self.visualizer = vis.Visualizer(self.save_frames_path)
        self.trajectory = trajectory
        self.total_time = total_time
        self.delta_t = delta_t
    
    def simulate(self):
        for frame in range(int(self.total_time//self.delta_t)):
            print("frame = ", frame, "     " , "time = ", frame * self.delta_t)
            self.visualizer.visualize(self.car, self.trajectory, frame)
            self.car.Drive(self.delta_t)
    
    def convert_to_mp4(self):
        os.chdir(self.save_frames_path)
        ffmpeg_command = "ffmpeg" + " " +  "-framerate"  + " " + str(1/self.delta_t) + " " + "-i" + " " + "\"frame-%04d\".jpg"+ \
         " " +  "out.mp4"
        os.system(ffmpeg_command)