import os
import cv2
from base_camera import BaseCamera
import time
#import scheddl
import sched_lib

class Camera(BaseCamera):
    video_source = 'lecture.avi'
    #video_source = 'movie.avi'  # ~10
    #video_source = 'soccer.avi' # ~10
    #video_source = 'street.avi' # 20-30
    #video_source = 'waves.avi'  # ~6
    #video_source = 'cartoon.avi'  # ~6



    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        '''
        dl_args = (
            20 * 1000 * 1000, # runtime in nanoseconds
            33 * 1000 * 1000, # deadline in nanoseconds
            33 * 1000 * 1000  # time period in nanoseconds
        )

        print("check 1")
        #scheddl.set_deadline(*dl_args)
        print("check 2")
        '''
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        cap = cv2.VideoCapture(Camera.video_source) 
        prev_frame_time = 0
        new_frame_time = 0
        
        '''
        # setup.py --help for more instructions
        # sample
        import scheddl

        dl_args = (
            20 * 1000 * 1000, # runtime in nanoseconds
            50 * 1000 * 1000, # deadline in nanoseconds
            50 * 1000 * 1000  # time period in nanoseconds
        )

        scheddl.set_deadline(*dl_args)

        while True:
            periodic_task(*args, **kwargs)
            scheddl.sched_yield()
        '''

        dl_args = (
            20 * 1000 * 1000, # runtime in nanoseconds
            33 * 1000 * 1000, # deadline in nanoseconds
            33 * 1000 * 1000  # time period in nanoseconds
        )

        print("Start configuring the scheduling policy.")
        #scheddl.set_deadline(*dl_args)
        #scheddl.set_deadline(20000000, 50000000, 50000000, scheddl.RESET_ON_FORK)
       
        ret = sched_lib.sched_setattr(33000000, 33000000, 31350000, 6) # 6 is for SCHED_DEADLINE
        if ret < 0:
            print("Failed switching to SCHED_DEADLINE.")
        else:
            print("Finished switching")
        
        c_start = time.time()
        while cap.isOpened():
            ret, frame = cap.read()

            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            # font which we will be using to display FPS 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            # time when we finish processing for this frame 
            new_frame_time = time.time() 
        
            fps = 1/(new_frame_time-prev_frame_time) 
            prev_frame_time = new_frame_time 
         
            fps = int(fps)  
            fps = str(fps)
            cv2.putText(frame, fps, (0, 30), font, 1, (100, 255, 0), 2, cv2.LINE_AA)      
            #print(fps)

            #time.sleep(0.025) # real-time speed for cv2
            #scheddl.sched_yield()
            #print("yeld afetr")
            #os.sched_yield()
            yield cv2.imencode('.jpg', frame)[1].tobytes()
            c_end = time.time()
            print("C = {}\tfps = {}".format(c_end-c_start, fps))
            os.sched_yield()
            c_start = time.time()
            #print("Afetr calling os.sched_yield()")
