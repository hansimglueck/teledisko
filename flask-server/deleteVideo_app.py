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
    with app.app_context():
        video_directory = '/media/alphi/BB42-5BFC/'
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)

        # Delete video files
        old_video_files = User.query.filter(User.createdAt <= one_hour_ago).all()
        
        for video_file in old_video_files:
            if video_file.videoFileName is not None:
                file_path = os.path.join(video_directory, video_file.videoFileName)
                
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    #
                    video_file.videoDeleted = True
                    db.session.commit()


def delete_old_videos():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_old_video_files, trigger='interval', minutes=60)
    scheduler.start()
    print("Start Scheduler to delete Videofiles")


if __name__ == '__main__':
    with app.app_context():
      

        delete_old_videos()
     
    app.run(debug=True, port=5010)
