from flask import Flask, render_template, request, redirect, url_for, make_response
from random import randint
from time import sleep
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2
import subprocess
import time 

db = SQLAlchemy()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
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
    # check if there was a user created in the last second
    while (User.query.filter(User.createdAt > datetime.utcnow().replace(second=0, microsecond=0)).first() is None):
        print ("waiting for qr code scan")
        sleep(1)
        pass
    return render_template('touchQrLoaded.html')


@app.route('/roteShow')
def roteShow():
     return render_template('roteShowStart.html')

@app.route('/RecordRoteShow')
def RecodRoteShow():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))
    start_time = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time.time() - start_time > 20:
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # merge audio and video
    video_file = 'output.mp4'
    audio_file = 'redShow.mp3'
    merged_file = 'merged.mp4'
    cmd = f'ffmpeg -i {video_file} -i {audio_file} -c:v copy -c:a aac -async 1 {merged_file}'
    subprocess.call(cmd, shell=True)

    # remove temporary files
    os.remove(video_file)
    #os.remove(audio_file)

    # Save the video file name to the database
    # Save videoReayToDownloadFlag to the Database
    session_id = request.cookies.get('id')
    user = User.query.filter_by(sessionId=session_id).first()
    user.videoFile = 'merged.mp4'
    user.videoReayToDownloadFlag = True
    db.session.commit()
     
    return render_template('roteShowEnde.html')



@app.route('/fonWelcome')
def fonWelcome():
    id = randint(0, 1000000)
    resp = make_response(render_template('fonWelcome.html'))
    resp.set_cookie('id', str(id))
    user = User(sessionId = str(id))
    db.session.add(user)
    db.session.commit()
    return resp



@app.route('/fonDownloadVideo')
def fonDownloadVideo():
  
   #Todo ABfragen ob video schon bereit ist
   #Todo Wenn ja springe zu fonDownloadVideo.html und ubergebe den downlaodlink als variable
    print("Warte das Video gerendert wird ")
    return redirect(url_for('fonDownloadVideo'))
    #return render_template('fonDownloadVideo.html')


if(__name__ == '__main__'):
    # uncomment once to reflect changes to the model (and delte database-file)
    # with app.app_context():
    #     print('Creating database tables...')
    #     db.create_all()
    #     print('Done.')
    app.run(debug=True)
