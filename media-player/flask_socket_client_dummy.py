from flask import Flask, render_template
from media_player import MediaPlayer

app = Flask(__name__)
media_player = MediaPlayer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    media_player.play()
    return render_template('play.html') # onload in der seite

@app.route('/playing')
def playing():
    media_player.wait_for_complete()  # Wait for the complete event to be set
    print("complete")
    return 'complete'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
