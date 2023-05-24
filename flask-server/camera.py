from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import time
from flask import url_for 

class Camera:
    def __init__(self):
        self.picam2 = None
        self.encoder = None
        self.output = None
        self.videoFileName = None
        self.videoFilePath = None
    
    def update(self):
        self.picam2 = Picamera2()
        

        controls = {"Contrast":2.0,
                    "Brightness":0.4,
                    "ExposureTime": 30000,
                    "AnalogueGain": 20.0
                    }
        video_config = self.picam2.create_video_configuration(main={"size": (1080, 1080)},controls=controls)
        
        
      
        self.picam2.configure(video_config)
        self.encoder = H264Encoder(10000000)#10MB
     


        self.videoFilePath = '/media/alphi/BB42-5BFC/'
        self.videoFileName = 'ElixirDisco-' + time.strftime("%Y%m%d-%H%M")+'.mp4'
        self.output = FfmpegOutput( self.videoFilePath + self.videoFileName, audio=True )


    def startVideoRecording(self):
        self.picam2.start_recording(self.encoder, self.output)

    def stopVideoRecording(self):
        self.picam2.stop_recording()
        self.picam2.close()
        
    def close_video(self):
        self.picam2.close()
        
 