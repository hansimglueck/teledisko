# views/touch.py
from flask import Blueprint, render_template, request, redirect, url_for, make_response
from camera import Camera
import time
from datetime import datetime
from time import sleep
from models import db, User
from time import sleep


myCamera = Camera()


touch_blueprint = Blueprint("touch", __name__)



@touch_blueprint.route('/')
def welcome():
    return render_template('touchWelcome.html')

@touch_blueprint.route('/touchWelcomeConfirm')
def touchWelcomeConfirm():
    return redirect(url_for('touchReally'))

@touch_blueprint.route('/touchReally')
def touchReally():
    return render_template('touchReally.html')

@touch_blueprint.route('/touchReallyConfirm')
def touchReallyConfirm():
    return redirect(url_for('touchDsgvo'))

@touch_blueprint.route('/touchDsgvo')
def touchDsgvo():
    return render_template('touchDSGVO.html')

@touch_blueprint.route('/touchDsgvoConfirm')
def touchDsgvoConfirm():
    return redirect(url_for('touchQrCode'))

@touch_blueprint.route('/touchQrCode')
def touchQrCode():
    print("QR")
    return render_template('touchQrCode.html')

@touch_blueprint.route('/touchQrLoaded')
def touchQrLoaded():
    session_id = request.cookies.get('id')
    print("QR - waiting for session id:", session_id)
    print("QR - waiting")

    # TODO: find a better way to do this
    # creates a while loop that will keep running until a 
    # User object is created with a "createdAt" attribute
    # that is greater than the current UTC datetime with
    # its seconds and microseconds set to zero.
    # I wait for fonWelcome to create a user object with a session id
    while (User.query.filter(User.createdAt > datetime.utcnow().replace(second=0, microsecond=0)).first() is None):
        print ("waiting for qr code scan")
        sleep(1)
        pass
    return render_template('touchRotOderBlau.html')


@touch_blueprint.route('/roteShow')
def roteShow():
     return render_template('roteShowStart.html')

@touch_blueprint.route('/RecordRoteShow')
def RecordRoteShow():

    #Video records for 10 Seconds
    myCamera.update()
    myCamera.startVideoRecording()
    time.sleep(120) 
    myCamera.stopVideoRecording()


    # Save the video file name to the database
    # Save videoReayToDownloadFlag to the Database
    session_id = request.cookies.get('id')
    user = User.query.filter_by(sessionId=session_id).first()
    user.videoFile = myCamera.videoFileName
    user.videoReayToDownloadFlag = True
    db.session.commit()

    time.sleep(2)

    last_entry = User.query.order_by(User.createdAt.desc()).first()

    if last_entry is not None:

        print(last_entry.videoFile)
        video_url = last_entry.videoFile
        print(video_url)
        return render_template('roteShowEnde.html',video_url=video_url)
    else:

        return"Die VideoUrl konnte nicht ausgelesen werden"



