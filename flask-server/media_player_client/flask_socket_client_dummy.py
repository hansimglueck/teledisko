import sys
sys.path.append('../')  # Hinzufügen des übergeordneten Verzeichnisses zum Python-Pfad
from flask import Flask, render_template, redirect, url_for
from media_player import MediaPlayer

app = Flask(__name__)
media_player = MediaPlayer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_red')
def play_red():
    media_player.load("red")
    media_player.play()
    return render_template('play.html',track_id="red") # onload in der seite

@app.route('/play_blue')
def play_blue():
    media_player.load("blue")
    media_player.play()
    return render_template('play.html',track_id="blue") # onload in der seite

@app.route('/stop')
def stop():
    media_player.stop()
    return redirect(url_for('index'))

@app.route('/playing')
def playing():
    media_player.wait_for_complete()  # Wait for the complete event to be set
    print("complete")
    return 'complete'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
