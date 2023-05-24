from flask import Flask, render_template, request, redirect, url_for, send_from_directory,abort
from config import Config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import subprocess
from media_player_client.media_player import MediaPlayer
import os
from datetime import datetime, timedelta


myMediaPlayer2 = MediaPlayer()


app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = 'static'
app.config['UPLOAD_FOLDER'] = '/media/alphi/BB42-5BFC/'
# app.config['UPLOAD_FOLDER'] = 'static/videos/'

app.config.from_object(Config)
db.init_app(app)


############################################################################
##################Insert  und validate  Password for Download ##############
############################################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':

        session_id = request.form['session_id']

        user = User.query.filter_by(sessionId=session_id).first()

        if user:
                
            if user.videoDeleted :

                return render_template('fon_video_deleted.html')
            
            elif user.downloaded :

                return render_template('fon_video_downloaded.html')
            
               # Video wurde mit diesem Password noch nicht  runtergeladen
            else:
               
                return redirect(url_for('prepare_download', session_id=user.sessionId))
            
        else:

            return render_template('fon_code_not_found.html')
        
    return render_template('fon_index.html')





############################################################################
###################2. Bereitstellung  des Video Downloadprozess ############
############################################################################

@app.route('/prepare_download/<session_id>')
def prepare_download(session_id):
    return render_template('fon_prepare_download.html', session_id=session_id)





############################################################################
###################3. Versendung  des Videofiles ##########################
############################################################################

@app.route('/download/<session_id>')
def download(session_id):
    user = User.query.filter_by(sessionId=session_id).first()

    if user and not user.downloaded:

        video_file = user.videoFileName


        try:
            # user.downloaded = True
            # db.session.commit()
            return send_from_directory(app.config['UPLOAD_FOLDER'], video_file, as_attachment=True)
    
        except Exception as e:
            # user.downloaded = False
            # db.session.commit()
            print(str(e))
            #abort(500, description="Error during file download")
            return render_template('fon_error_video_downloaded.html')

    else:
       
        return render_template('fon_video_downloaded.html')

    



############################################################################
###################3. Danke  und Verabschiedung  ##########################
############################################################################
@app.route('/thanks')
def thanks():
    return render_template('fon_download_success.html')




############################################################################
###################     WARTUNG  ##########################
############################################################################


@app.route('/shutdown')
def shutdown():
    return render_template('wartung_elixyr_disco.html')

@app.route('/stop_record')
def stop_show():
    myMediaPlayer2.stop()
    return render_template('wartung_elixyr_disco.html')


@app.route('/alles_ausschalten')
def alles_ausschalten():
     # animation
    result = subprocess.run(["ssh", "pi@telepi42", "sudo shutdown -h now"], shell=False)
    print(result)
    # netzwerk
    result = subprocess.run(["ssh", "pi@uiraspi2", "sudo shutdown -h now"], shell=False)
    print(result)
    # touch and camera
    result = subprocess.run(["ssh", "pi@telepi2", "sudo shutdown -h now"], shell=False) 
    print(result)

    return render_template('wartung_elixyr_disco.html')



@app.route('/reset_alles')
def reset_alles():
     # animation
    result = subprocess.run(["ssh", "pi@telepi42", "sudo shutdown -r now"], shell=False)
    print(result)
    # netzwerk
    result = subprocess.run(["ssh", "pi@uiraspi2", "sudo shutdown -r now"], shell=False)
    print(result)
    # touch and camera
    result = subprocess.run(["ssh", "pi@telepi2", "sudo shutdown -r now"], shell=False) 
    print(result)

    return render_template('wartung_elixyr_disco.html')





@app.route('/soft_reset')
def soft_reset():
     # animation
    result = subprocess.run(["ssh", "pi@telepi42", "sudo systemctl --user restart media-socket-server.service"], shell=False)
    print(result)

    # TouchSceen - Recoord Video
    result = subprocess.run(["ssh", "pi@telepi2", "sudo systemctl --user restart teleflask-server.service"], shell=False) 
    print(result)
    #Chromium Browser
    result = subprocess.run(["ssh", "pi@telepi2", "sudo systemctl --user restart kiosk.service"], shell=False) 
    print(result)

    return render_template('wartung_elixyr_disco.html')



@app.route('/delete_videos')
def delete_videos():
     # animation
    video_directory = '/media/alphi/BB42-5BFC/'
    current_time = datetime.now()
    one_hour_ago = current_time - timedelta(hours=1)

    # Delete video files
    old_video_files = User.query.filter(User.createdAt <= one_hour_ago).all()
    for video_file in old_video_files:
        if video_file.videoFileName is not None:
            file_path = os.path.join(video_directory, video_file.videoFileName)
            print(file_path)
            if os.path.isfile(file_path):
                os.remove(file_path)
                video_file.videoDeleted= True
                db.session.commit()

    return render_template('wartung_elixyr_disco.html')



if (__name__ == '__main__'):
    app.run(debug=True, port=8081, host ='0.0.0.0')
