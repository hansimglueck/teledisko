from flask import Flask, render_template, request, redirect, url_for,send_from_directory
from config import Config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db, User

    
app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = 'static'
app.config.from_object(Config)
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session_id = request.form['session_id']
        user = User.query.filter_by(sessionId=session_id).first()
        if user:
            return redirect(url_for('video_page', session_id=user.sessionId))
        else:
            return render_template('fon_code_not_found.html')
    return render_template('fon_index.html')

@app.route('/video/<session_id>')
def video_page(session_id):
    user = User.query.filter_by(sessionId=session_id).first()
    if user:
        # If user.videoFile starts with 'static/', remove 'static/' from the beginning
        video_file = user.videoFile[7:] if user.videoFile.startswith('static/') else user.videoFile
        video_link = url_for('static', filename=video_file)
        return render_template('fonDownloadVideo.html', video_link=video_link,session_id=session_id)
    else:
        return redirect(url_for('index'))

@app.route('/download/<session_id>')
def download(session_id):
    user = User.query.filter_by(sessionId=session_id).first()
    if user and not user.downloaded:
        user.downloaded = True
        db.session.commit()

        video_file = user.videoFile[7:] if user.videoFile.startswith('static/') else user.videoFile

        return send_from_directory(app.config['STATIC_FOLDER'], video_file, as_attachment=True)
    else:
        return "This video has already been downloaded."



if (__name__ == '__main__'):
    # with app.app_context():
    #   print('Creating database tables...')
    #   db.create_all()
    #   print('Done.')
    app.run(debug=True, port= 8080)

