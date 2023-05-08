from flask import Flask, render_template, request, redirect, url_for, make_response
from random import randint
from time import sleep
import time
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from camera import Camera


app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = 'static'

########################### SQL-DATABASE###################################
db = SQLAlchemy()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'teledisko.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    __tablename__ = 'teledisko'
    id = db.Column(db.Integer, primary_key=True)
    videoFile = db.Column(db.String(120), unique=False)   
    sessionId = db.Column(db.String(120), unique=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    qrLoadedFlag = db.Column(db.Boolean, default=False)
    videoReayToDownloadFlag = db.Column(db.Boolean, default=False)

db.init_app(app)   


#########################################################################

########################### CAMERA###################################

myCamera = Camera()




@app.route('/')
def welcome():
    return render_template('touchWelcome.html')

@app.route('/touchWelcomeConfirm')
def touchWelcomeConfirm():
    return redirect(url_for('touchReally'))

@app.route('/touchReally')
def touchReally():
    return render_template('touchReally.html')

@app.route('/touchReallyConfirm')
def touchReallyConfirm():
    return redirect(url_for('touchDsgvo'))

@app.route('/touchDsgvo')
def touchDsgvo():
    return render_template('touchDSGVO.html')

@app.route('/touchDsgvoConfirm')
def touchDsgvoConfirm():
    return redirect(url_for('touchQrCode'))

@app.route('/touchQrCode')
def touchQrCode():
    print("QR")
    return render_template('touchQrCode.html')

@app.route('/touchQrLoaded')
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


@app.route('/roteShow')
def roteShow():
     return render_template('roteShowStart.html')

@app.route('/RecordRoteShow')
def RecordRoteShow():

    #Video records for 10 Seconds
    myCamera.update()
    myCamera.startVideoRecording()
    time.sleep(10) 
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

    print(last_entry.videoFile)
    video_url = last_entry.videoFile
    print(video_url)
    return render_template('roteShowEnde.html',video_url=video_url)






"""
 
     _  _   _____ ___  _   _ 
   _| || |_|  ___/ _ \| \ | |
  |_  ..  _| |_ | | | |  \| |
  |_      _|  _|| |_| | |\  |
    |_||_| |_|   \___/|_| \_|
                             
 
"""
@app.route('/fonWelcome')
def fonWelcome():
     
        id = str(randint(0, 1000000))
        user = User(sessionId=id)
        db.session.add(user)
        db.session.commit()
         
        user = User.query.filter_by(sessionId=id).first()
        # Set the session ID as a cookie
        resp = make_response(render_template('fonWelcome.html'))
        resp.set_cookie('id', id)

        return resp




@app.route('/fonDownloadVideo')
def fonDownloadVideo():
    session_id = request.cookies.get('id')
    user = User.query.filter_by(sessionId=session_id).first()

    # Wait until the user's video is ready for download
    while not user.videoReayToDownloadFlag:
        print("Waiting for download link...")
        sleep(1)
        user = User.query.filter_by(sessionId=session_id).first()

    # Set the videoReadyToDownloadFlag to False so that the user cannot download it again
    user.videoReayToDownloadFlag = False
    db.session.commit()

    # Generate the download link and pass it to the template
    video_link = url_for('static', filename='videos/test.webm')
    return render_template('fonDownloadVideo.html', video_link=video_link)



if(__name__ == '__main__'):
    # uncomment once to reflect changes to the model (and delte database-file)
    # with app.app_context():
    #     print('Creating database tables...')
    #     db.create_all()
    #     print('Done.')
    app.run(debug=True)
