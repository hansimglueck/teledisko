from flask import Flask, render_template, request, redirect, url_for, make_response
from random import randint
from time import sleep
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'teledisko.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    __tablename__ = 'teledisko'
    id = db.Column(db.Integer, primary_key=True)
    videoFile = db.Column(db.String(120), unique=False)   
    sessionId = db.Column(db.String(120), unique=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    qrLoadedFlag = db.Column(db.Boolean, default=False)

db.init_app(app)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/welcomeConfirm')
def welcomeConfirm():
    return redirect(url_for('really'))

@app.route('/really')
def really():
    return render_template('really.html')

@app.route('/reallyConfirm')
def reallyConfirm():
    return redirect(url_for('dsgvo'))

@app.route('/dsgvo')
def dsgvo():
    return render_template('DSGVO.html')

@app.route('/dsgvoConfirm')
def dsgvoConfirm():
    return redirect(url_for('qrCode'))

@app.route('/qrCode')
def qrCode():
    print("QR")
    return render_template('qrCode.html')

@app.route('/qrLoaded')
def qrLoaded():
    print("QR - waiting")
    # TODO: find a better way to do this
    # check if there was a user created in the last second
    while (User.query.filter(User.createdAt > datetime.utcnow().replace(second=0, microsecond=0)).first() is None):
        print ("waiting for qr code scan")
        sleep(1)
        pass
    return render_template('qrLoaded.html')

@app.route('/fonWelcome')
def fonWelcome():
    id = randint(0, 1000000)
    resp = make_response(render_template('fonWelcome.html'))
    resp.set_cookie('id', str(id))
    user = User(sessionId = str(id))
    db.session.add(user)
    db.session.commit()
    return resp

if(__name__ == '__main__'):
    # uncomment once to reflect changes to the model (and delte database-file)
    # with app.app_context():
    #     print('Creating database tables...')
    #     db.create_all()
    #     print('Done.')
    app.run(debug=True)
