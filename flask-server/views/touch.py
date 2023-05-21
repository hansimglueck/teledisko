# views/touch.py
from flask import Blueprint, render_template, request, redirect, url_for, make_response
import time
from datetime import datetime
from time import sleep
from models import db, User
from time import sleep
from random import randint
from media_player_client.media_player import MediaPlayer
from camera import Camera
from door import Door
import random
import string
from logger import setup_logger




############################################################################
random_code = None    # variable stores unic  generated code for  user
############################################################################
logger = setup_logger("flaskserver") # Debbuging Tool
############################################################################
selectedShow = "" # "red" or "blue" for Medoaiplayer
################################## INIT DOOR-SENSOR   ######################
myDoor = Door()           # SENSOR OPEN - CLOSE
################################## INIT CAMERA   ###########################
myCamera = Camera()       # AV-RECORDING
################################## INIT SOCKET CLIENT MEDIAPLAYER   ########
myMediaPlayer = MediaPlayer()
################################## INIT  BLUE_PRINT ########################
touch_blueprint = Blueprint("touch", __name__)
############################################################################





############################################################################
############################ 1. WANNA CHANGE ################################
############################################################################
@touch_blueprint.route('/')
def wanna_change():

    logger.debug("1_wanna_change")

    onClick_Goto_route = "touch.info_wanna_change"  # Prepend blueprint name to the route

    return render_template('1_wanna_change.html', onClick_Goto_route=onClick_Goto_route)



############################################################################
############################ 2. INFO WANNA CHANGE ##########################
############################################################################
@touch_blueprint.route('/info_wanna_change')
def info_wanna_change():

    print("2_info_wanna_change")

    onClick_Goto_route = "touch.strong_or_soft"  # Prepend blueprint name to the route

    return render_template('2_info_wanna_change.html', onClick_Goto_route=onClick_Goto_route)



############################################################################
############################ 3. STRONG OR  SOFT ############################
############################################################################
@touch_blueprint.route('/strong_or_soft')
def strong_or_soft():
    
    print("3_strong_or_soft")

    onClick_Goto_route = "touch.DSGVO"  # Prepend blueprint name to the route

    return render_template('3_strong_or_soft.html', onClick_Goto_route=onClick_Goto_route)



##########################################################################
############################ 3b. RED OR  BLUE ############################
##########################################################################
@touch_blueprint.route('/DSGVO/<selected_Show>')
def DSGVO(selected_Show):


    #TGete selectedShow (RED or BLUE)  is needed later in the route record_show
    # to send via Mediaplayer via Socket 
    global selectedShow 
    selectedShow = selected_Show
    print("The User seletec ShoW :") 
    print(selectedShow)
    

    print("3a_DSGVO")

    onClick_Goto_route = "touch.get_qr_and_wifi"  # Prepend blueprint name to the route

    return render_template('3b_DSGVO.html', onClick_Goto_route=onClick_Goto_route)



##########################################################################
############################ 3c. GET QR AND WIFI ############################
##########################################################################
@touch_blueprint.route('/get_qr_and_wifi')
def get_qr_and_wifi():


    print("3c_get_qr_and_wifi")

    onClick_Goto_route = "touch.get_code_for_video"  # Prepend blueprint name to the route

    return render_template('3c_get_qr_and_wifi.html', onClick_Goto_route=onClick_Goto_route)



############################################################################
############################ 4. GET CODE FOR VIDEO  ########################
############################################################################
@touch_blueprint.route('/get_code_for_video')
def get_code_for_video():
    
    print("4_get_code_for_video")
    

    # Generate a random number with 2 digits
    random_number = random.randint(10, 99)

    # Generate a random string with 2 characters
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.ascii_lowercase, k=2))

    # Combine the random number and random characters with a space in between
    random_code = f"{random_number}{random_chars}"

    # Check if the random code already exists in the database
    while User.query.filter_by(sessionId=random_code).first() is not None:
        print("Random code already exists in the database. Regenerating...")
        # Regenerate the random code
        random_number = random.randint(10, 99)
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.ascii_lowercase, k=2))
        random_code = f"{random_number}{random_chars}"

    print("Current Code:")
    print(random_code)
    
    # Create a new user with the session_id
    user = User(sessionId=random_code)

    # Add the new user to the session
    db.session.add(user)

    # Commit the changes to the database
    db.session.commit()


    # Abfrage  of password wirklich  in die datenbak gespeichert worde
    user = User.query.filter_by(sessionId=random_code).first()

    # wenn ja
    if user is not None:
        
        print("Random Code:")
        print(user.sessionId)

        # Set the session ID as a cookie
        onClick_Goto_route = "touch.get_ready_for_show"  # Prepend blueprint name to the route


        return  render_template('4_get_Code_for_Video.html',code=user.sessionId, onClick_Goto_route=onClick_Goto_route)
        
    else:
        # handle the case where no user object was found
        print("Aktuelle User Id ist nicht vergeben")
        return "ERROR: Die Session konnte nicht abgerufen werden!!!!!"



############################################################################
############################ 5. GET READY FOR SHOW #########################
############################################################################
@touch_blueprint.route('/get_ready_for_show')
def get_ready_for_show():
    
 
    print("5_get_ready_for_show")

    onLoad_Goto_route = "touch.wait_for_Door"  # Prepend blueprint name to the route

    return render_template('5_get_ready_for_Show.html', onLoad_Goto_route=onLoad_Goto_route)




####################################################################
############################ 6.WAIT FOR DOOR #########################
####################################################################
@touch_blueprint.route('/wait_for_Door')
def wait_for_Door():
     
     global selectedShow 
     print("Der  Gast hat folgende Show ausgewaehlt:") 
     print(selectedShow)

    #DIE TUER IST GESCHLossen
     print("Dir Tuer ist geschlossen")
     print("Oeffne die Tuer ")
     print("Und schliesse Sie")
     print ("Damit die Show beginnt")

     #########################
     myDoor.wait_for_closing() 
     #########################
     
     onLoad_Goto_route = "touch.record_show"  # Prepend blueprint name to the route
     return render_template('6_please_wait_for_your_Turn.html', onLoad_Goto_route=onLoad_Goto_route)



#####################################################################
############################ 7. RECORD SHOW #########################
#####################################################################
@touch_blueprint.route('/record_show')
def record_show():
   
    
   
    myMediaPlayer.load(selectedShow)
    myMediaPlayer.play()  # Send  via Socket to Raspi2 that he should start
    
    #RECO
    ######################################
    print("starting Camera for recording")
    myCamera.update()
    myCamera.startVideoRecording()
    ######################################

    
    myMediaPlayer.wait_for_complete() # Blockking



    ######################################
    print("stopping recording")
    myCamera.stopVideoRecording()
    print("stopped")
    ######################################

    # Save the video file name  and path to the database
    # Save videoReayToDownloadFlag to the Database

 
    session_id = random_code

    user = User.query.filter_by(sessionId=session_id).first()

    print(myCamera.videoFileName)
    print(myCamera.videoFilePath)

    user.videoFile = myCamera.videoFileName
    user.videoFilePath = myCamera.videoFilePath
    
    user.videoReayToDownloadFlag = True
    db.session.commit()

    
    onClick_Goto_route = "touch.info_wanna_change"  # Prepend blueprint name to the route

    return render_template('1_wanna_change.html', onClick_Goto_route=onClick_Goto_route)
     


