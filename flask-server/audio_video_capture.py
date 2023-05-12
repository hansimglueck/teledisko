#!/usr/bin/python3
import time
from camera import Camera
from flask import Flask

app = Flask(__name__)

myCamera = Camera()

@app.route('/')
def hello():
    print("Starting camera for recording")

    # Video records for 10 seconds
    myCamera.update()
    myCamera.startVideoRecording()
    time.sleep(10)
    print("Stopping recording")
    myCamera.stopVideoRecording()
    print("Stopped")

    return 'Record-End'

if __name__ == '__main__':
    app.run(debug=True, port=6060)
