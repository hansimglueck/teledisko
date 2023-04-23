from flask import Flask, render_template, request, redirect, url_for, make_response
from random import randint
# Hallo Hans
import os

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
