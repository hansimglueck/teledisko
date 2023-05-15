# views/touch.py
from flask import Blueprint, render_template, request, redirect, url_for, make_response

import time
from datetime import datetime
from time import sleep
from models import db, User
from time import sleep
from random import randint

from media_player import MediaPlayer
from camera import Camera
from door import Door

################################## DOOR-SENSOR   #####################################
myDoor = Door()
################################## INIT CAMERA   #####################################
myCamera = Camera()
################################## SOcket Mediaplayer   #####################################
myMediaPlayer = MediaPlayer()
################################# WAIT FUNCTION ###########################################
def wait_for(condition_function, timeout=10, poll_interval=1):
    start_time = time.time()

    while not condition_function():
        if time.time() - start_time > timeout:
            raise TimeoutError("Timeout while waiting for condition.")
        sleep(poll_interval)
################################# INT  BLUE_PRINT ###########################################

touch_blueprint = Blueprint("touch", __name__)

############################ 1. WANNA CHANGE ################################
@touch_blueprint.route('/')
def wanna_change():
    print("wanna_change")
    return render_template('1_wanna_change.html')








@touch_blueprint.route('/WelcomeConfirm')
def WelcomeConfirm():
    return redirect(url_for('touch.Really'))

@touch_blueprint.route('/Really')
def Really():
    return render_template('touchReally.html')

@touch_blueprint.route('/ReallyConfirm')
def ReallyConfirm():
    return redirect(url_for('touch.Dsgvo'))


@touch_blueprint.route('/Dsgvo')
def Dsgvo():
    return render_template('touchDSGVO.html')

@touch_blueprint.route('/DsgvoConfirm')
def DsgvoConfirm():
    return redirect(url_for('touch.GetCode'))


@touch_blueprint.route('/GetCode')
def GetCode():
     
        id = str(randint(0, 1000000))
        print("Aktuelle Code:")
        print(id)
        user = User(sessionId=id)
        db.session.add(user)
        db.session.commit()
         
        user = User.query.filter_by(sessionId=id).first()

        if user is not None:
             # do something with the user object
             print("Random Code:")
             print(user.sessionId)
            # Set the session ID as a cookie
             resp = make_response(render_template('touchGetCode.html',code=user.sessionId))
             resp.set_cookie('id', id)
             return resp
        else:
             # handle the case where no user object was found
             print("Aktuelle User Id ist nicht vergeben")
             return "ERROR: Die Session konnte nicht abgerufen werden!!!!!"

@touch_blueprint.route('/RotOderBlau')
def RotOderBlau():
     return render_template('touchRotOderBlau.html')

@touch_blueprint.route('/preShow')
def preShow():
     return render_template('preShow.html')

@touch_blueprint.route('/wait_for_Door')
def wait_for_Door():
     
    #DIE TUER IST GESCHLossen
     print("Dir Tuer ist geschlossen")
     print("Oeffne die Tuer ")
     print("Und schliesse Sie")
     print ("Damit die Show beginnt")
     
     myDoor.wait_for_closing() 
     return render_template('roteShowStart.html')

@touch_blueprint.route('/RecordRoteShow')
def RecordRoteShow():

    myMediaPlayer.play() # Send  via Socket to Raspi2 that he should start

    print("starting Camera for recording")
    myCamera.update()
    myCamera.startVideoRecording()

    
    myMediaPlayer.wait_for_complete()
    print("stopping recording")
    myCamera.stopVideoRecording()
    print("stopped")


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



