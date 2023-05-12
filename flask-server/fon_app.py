from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, User




 # Make sure the video file is located in the correct directory
# Example: If the file is in the same directory as app.py, use the following code:

app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = 'static'
app.config.from_object(Config)
db.init_app(app)  # Keep this line here in the app.py file


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session_id = request.form['session_id']
        user = User.query.filter_by(sessionId=session_id).first()
        if user:
            return redirect(url_for('video_page', video_link=user.videoFile))
        else:
            return render_template('fon_code_not_found.html')
    return render_template('fon_index.html')

@app.route('/<video_link>')
def video_page(video_link):
    return render_template('fonDownloadVideo.html', video_link=video_link)



if (__name__ == '__main__'):
    # Uncomment once to reflect changes to the model (and delete the database-file)
    # with app.app_context():
    #     print('Creating database tables...')
    #     db.create_all()
    #     print('Done.')
    app.run(debug=True, port= 8000)