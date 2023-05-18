from flask import Flask, render_template, request, redirect, url_for, send_from_directory
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
            if user.downloaded:
                return render_template('fon_video_downloaded.html')
            else:
                return redirect(url_for('prepare_download', session_id=user.sessionId))
        else:
            return render_template('fon_code_not_found.html')
    return render_template('fon_index.html')
    # return render_template('fon_download_success.html')





@app.route('/prepare_download/<session_id>')
def prepare_download(session_id):
    return render_template('prepare_download.html', session_id=session_id)


@app.route('/download/<session_id>')
def download(session_id):
    user = User.query.filter_by(sessionId=session_id).first()
    if user and not user.downloaded:
        video_file = user.videoFile[7:] if user.videoFile.startswith('static/') else user.videoFile
        try:
            response = send_from_directory(app.config['STATIC_FOLDER'], video_file, as_attachment=True)
            user.downloaded = True
            db.session.commit()
            return response
        except Exception as e:
            print(str(e))
            abort(500, description="Error during file download")
    else:
        return render_template('fon_video_downloaded.html')

@app.route('/thanks')
def thanks():
    return render_template('fon_download_success.html')

if (__name__ == '__main__'):
    app.run(debug=True, port= 8082 , host ='0.0.0.0')