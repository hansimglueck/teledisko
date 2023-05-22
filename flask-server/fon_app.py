from flask import Flask, render_template, request, redirect, url_for, send_from_directory,abort
from config import Config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import subprocess

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

                # Video wurde mit diesem Password schonmal runtergeladen
            if user.downloaded or user.videoDeleted: 

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
            user.downloaded = True
            db.session.commit()
            return send_from_directory(app.config['UPLOAD_FOLDER'], video_file, as_attachment=True)
    
        except Exception as e:
            user.downloaded = False
            db.session.commit()
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

    return render_template('Nachdem SuperReset - muss du dich wieder in das Elixyr Netzwerk anmelden')



if (__name__ == '__main__'):
    app.run(debug=True, port=8081, host ='0.0.0.0')
