from flask import Flask, redirect, url_for
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

# Create class
class AVideoRecorder:
    def __init__(self):
        self.picam2 = None
        self.encoder = None
        self.output = None
    
    def update(self):
        self.picam2 = Picamera2()
        

        controls = {"Contrast": 0.5, "ExposureTime": 10000, "AnalogueGain": 22.0}
        
        video_config = self.picam2.create_video_configuration(main={"size": (640, 480)},controls=controls)
        self.picam2.configure(video_config)
        self.encoder = H264Encoder(10000000)
        self.output = FfmpegOutput('/media/alphi/INTENSO/test-' +time.strftime("%Y%m%d-%H%M%S")+'.mp4', audio=True )

    def start_video(self):
        self.picam2.start_recording(self.encoder, self.output)

    def stop_video(self):
        self.picam2.stop_recording()
        self.picam2.close()
        
    def close_video(self):
        self.picam2.close()
        

# Create Flask app
app = Flask(__name__)

# Create an instance of AVideoRecorder
avRecorder = AVideoRecorder()


#Route of index
@app.route('/')
def index():
    #return "This is the beginning of a Flask Av Recording App"
    return redirect(url_for('start'))

# Route to start recording
@app.route('/start')
def start():
    avRecorder.update()
    avRecorder.start_video()
    time.sleep(10)
    avRecorder.stop_video()
    return redirect(url_for('stop'))
   

# Route of stop Recording
@app.route('/stop')
def stop():
   return "The video should now saved on the usb stick"


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
