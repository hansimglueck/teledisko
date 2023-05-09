from flask import Flask, render_template, request, redirect, url_for, make_response
from config import Config
from views.touch import touch_blueprint
from views.fon import fon_blueprint
from models import db


app = Flask(__name__, static_url_path='/static')
app.config['STATIC_FOLDER'] = 'static'

# Config for SqlAlcheny
app.config.from_object(Config)

db.init_app(app)   







if(__name__ == '__main__'):
    # uncomment once to reflect changes to the model (and delte database-file)
    # with app.app_context():
    #     print('Creating database tables...')
    #     db.create_all()
    #     print('Done.')
    app.run(debug=True)
