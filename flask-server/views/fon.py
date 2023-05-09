from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models import db,User
from time import sleep
from random import randint

fon_blueprint = Blueprint("fon", __name__)



@fon_blueprint.route('/Welcome')
def Welcome():
     
        id = str(randint(0, 1000000))
        print("Aktuelle SesiionId:")
        print(id)
        user = User(sessionId=id)
        db.session.add(user)
        db.session.commit()
         
        user = User.query.filter_by(sessionId=id).first()

        if user is not None:
             # do something with the user object
             print("Random Session_ID:")
             print(user.sessionId)
            # Set the session ID as a cookie
             #resp = make_response(redirect(url_for('fonDownloadVideo')))
             resp = make_response(render_template('fonWelcome.html',aktuelleSessionId=user.sessionId))
             resp.set_cookie('id', id)
             return resp
        else:
             # handle the case where no user object was found
             print("Aktuelle User Id ist nicht vergeben")
             return "ERROR: Die Session konnte nicht abgerufen werden!!!!!"



@fon_blueprint.route('/DownloadVideo')
def nDownloadVideo():
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