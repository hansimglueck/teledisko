from flask import Flask
from config import Config
from models import db
from views.touch import touch_blueprint
from views.fon import fon_blueprint

app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = 'static'
app.config.from_object(Config)

host = '0.0.0.0'  # Lauschen auf Anfragen von beliebigen IPs

app.register_blueprint(touch_blueprint)
app.register_blueprint(fon_blueprint)

db.init_app(app)  # Keep this line here in the app.py file

if (__name__ == '__main__'):
    # Uncomment once to reflect changes to the model (and delete the database-file)
    # with app.app_context():
    #     print('Creating database tables...')
    #     db.create_all()
    #     print('Done.')
    app.run(debug=True, port=8000)

