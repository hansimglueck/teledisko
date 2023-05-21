import os
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from apscheduler.schedulers.background import BackgroundScheduler


# Assuming you have a directory where the video files are stored
video_directory = '/path/to/video/files/'


def delete_old_video_files():
    # Get the current time
    current_time = datetime.now()

    # Calculate the time one hour ago
    one_hour_ago = current_time - timedelta(hours=1)

    # Query the database for video files older than 1 hour or marked as downloaded
    old_video_files = User.query.filter(db.or_(User.createdAt <= one_hour_ago, User.downloaded == True)).all()

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
