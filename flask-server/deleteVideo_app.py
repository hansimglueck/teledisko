import os
from datetime import datetime, timedelta
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, User



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def delete_old_video_files():

    video_directory = '/media/alphi/BB42-5BFC/'

    # Get the current time
    current_time = datetime.now()

    # Calculate the time one hour ago
    one_hour_ago = current_time - timedelta(hours=1)

    # Query the database for video files older than 1 hour 
    old_video_files = User.query.filter(db.or_(User.createdAt <= one_hour_ago)).all()

    # Iterate over the video files and delete them from the directory
    for video_file in old_video_files:
        file_path = os.path.join(video_directory, video_file.videoFileName)

        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)
            # Update the deletedVideo field in the database
            video_file.deletedVideo = True
            db.session.commit()

def delete_old_videos():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_old_video_files, trigger='interval', hours=1)
    scheduler.start()

if __name__ == '__main__':
    with app.app_context():
        delete_old_videos()
    app.run(debug=True, port=5005)
