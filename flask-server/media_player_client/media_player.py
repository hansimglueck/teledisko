import threading
import socket
import configparser

class MediaPlayer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../../config.ini')
        self.host = config['MediaPlayer']['IP']
        self.port = int(config['MediaPlayer']['Port'])
        self.response = None
        self.response_received = threading.Event()
        self.complete_event = threading.Event()

    def load(self, track):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = f'load {track}'
            s.sendall(message.encode('utf-8'))

    def play(self):
        def play_thread():
            self.complete_event.clear()  # Clear the complete event before starting playback
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(b'play')
                self.response = s.recv(1024).decode('utf-8')
                self.response_received.set()
                self.set_complete_event()

        threading.Thread(target=play_thread).start()

    def pause(self):
        pass

    def stop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = f'stop'
            s.sendall(message.encode('utf-8'))
        pass

    def wait_for_complete(self):
        self.complete_event.wait()

    def wait_for_response(self):
        self.response_received.wait()

    def set_complete_event(self):
        self.complete_event.set()