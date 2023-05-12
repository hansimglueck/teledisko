import socketserver
import configparser
import time

class PlayerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')

        if self.data.startswith('load'):
            track_id = self.data.split(' ')[1]
            print("Loading track with ID:", track_id)
            # self.request.sendall(b'complete')

        elif self.data == 'play':
            print("Starting playback")
            time.sleep(7)
            print("Playback completed")
            self.request.sendall(b'complete')

        elif self.data == 'pause':
            print("Pausing playback")
            # self.request.sendall(b'complete')

        elif self.data == 'stop':
            print("Stopping playback")
            # self.request.sendall(b'complete')

        else:
            print("Invalid command received")

def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')

    host = config['Player']['IP']
    port = int(config['Player']['Port'])
    print(port, host)
    server = socketserver.TCPServer((host, port), PlayerHandler)

    print("Player is ready.")

    server.serve_forever()

if __name__ == "__main__":
    main()
