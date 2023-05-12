import socket
import configparser

def handle_complete():
    print("Playback completed. Performing callback action.")

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    host = config['Player']['IP']
    port = int(config['Player']['Port'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            command = input("Enter command (load, play, pause, stop): ")

            if command == 'load':
                track_id = input("Enter track ID: ")
                full_command = 'load {}'.format(track_id)
                s.sendall(full_command.encode('utf-8'))

            elif command == 'play':
                s.sendall(b'play')

            elif command == 'pause':
                s.sendall(b'pause')

            elif command == 'stop':
                s.sendall(b'stop')

            elif command == 'exit':
                break

            response = s.recv(1024).decode('utf-8')

            if response == 'complete':
                handle_complete()

if __name__ == "__main__":
    main()
