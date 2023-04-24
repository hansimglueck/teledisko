from flask import Flask, render_template, request, redirect, url_for, make_response
from random import randint
from time import sleep

# Hallo Hans
import os

qrLoadedFlag = False

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
    while (not qrLoadedFlag):
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