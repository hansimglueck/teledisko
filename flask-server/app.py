from flask import Flask, render_template, request, redirect, url_for, make_response
from random import randint
from time import sleep
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'teledisko.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'teledisko'
    id = db.Column(db.Integer, primary_key=True)
    videoFile = db.Column(db.String(120), unique=False, nullable=False)   
    session = db.Column(db.String(120), unique=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    qrLoadedFlag = db.Column(db.Boolean, default=False)



app = Flask(__name__)

# Startseite
@app.route('/')
def welcome():
    # generate random numeric value between 0 and 1000000
    # and use it as a session id
    id = randint(0, 1000000)
    resp = make_response(render_template('welcome.html'))
    resp.set_cookie('id', str(id))
    return resp

@app.route('/welcomeConfirm')
def welcomeConfirm():
    return redirect(url_for('really'))

@app.route('/really')
def really():
    return render_template('really.html', id=request.cookies.get('id'))

@app.route('/reallyConfirm')
def reallyConfirm():
    return redirect(url_for('dsgvo'))

@app.route('/dsgvo')
def dsgvo():
    return render_template('DSGVO.html', id=request.cookies.get('id'))

@app.route('/dsgvoConfirm')
def dsgvoConfirm():
    return render_template('qrCode.html')

@app.route('/qrCode')
def qrCode():
    # generate session for user and persist to database
    # reset qrLoadedFlag
    return render_template('qrCode.html')

@app.route('/qrLoaded')
def qrLoaded():
    while (not True):
        # read qrLoadedFlag from database (will be set when fon open fonWelcome)
        print ("waiting for qr code scan")
        # delay for 1 second
        sleep(1)
        pass
    return render_template('qrLoaded.html')

# fon
@app.route('/fonWelcome')
def fonWelcome():
    # set qrLoadedFlag in database to true
    return render_template('fonWelcome.html')

if(__name__ == '__main__'):
   
    with app.app_context():
       print('Creating database tables...')
       db.create_all()
       print('Done.')
    app.run(debug=True)