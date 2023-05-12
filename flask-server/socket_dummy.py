from flask import Flask, render_template
import socket
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
host = config['Player']['IP']
port = int(config['Player']['Port'])


# Flask-App erstellen
app = Flask(__name__)

choice = 'x'

@app.route('/a')
def a():
    # Hier kommt der Code hin, der passiert, wenn der player fertig ist
    global choice
    choice = 'a'
    return 'A'

@app.route('/b')
def b():
    # Hier kommt der Code hin, der passiert, wenn der player fertig ist
    global choice
    print(choice)
    choice = 'b'
    return 'B'

@app.route('/test')
def test():
    # Hier kommt der Code hin, der passiert, wenn der player fertig ist
    global choice
    print(choice)
    return choice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    # startRecord()
    # socket.sendPlay()
    return render_template('play.html')

@app.route('/complete')
def complete():
    # Hier kommt der Code hin, der den player startet
    # startRecord()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.connect((host, port))
        s.sendall(b'play')
        response = s.recv(1024).decode('utf-8')
        if response == 'complete':
            print("Playback completed. Performing callback action.")

    # stopRecord()

    return 'player completed!'


# Server starten
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
