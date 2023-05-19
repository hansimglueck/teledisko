import socketserver
import configparser
import time
import pygame
import subprocess
import threading

red_wav = "/home/pi/teledisko/media-player/sound/red230519.wav"
blue_wav = "/home/pi/teledisko/media-player/sound/blue230519.wav"
red_video = "/home/pi/teledisko/media-player/video/TM.mov"
blue_video = "/home/pi/teledisko/media-player/video/Elixyr_Logo_blue.mov"
loaded = "red"
stop_playback = False

class PlayerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global loaded, stop_playback
        self.data = self.request.recv(1024).strip().decode('utf-8')

        if self.data.startswith('load'):
            track_id = self.data.split(' ')[1]
            print("Loading track with ID:", track_id)
            loaded = track_id

        elif self.data == 'play':
            print("Starting playback", loaded)
            if loaded == "red":
                sound = pygame.mixer.Sound(red_wav)
                video_file = red_video
            else:
                sound = pygame.mixer.Sound(blue_wav)
                video_file = blue_video

            play_audio_thread = threading.Thread(target=play_audio, args=(sound,))
            play_audio_thread.start()

            play_video(video_file)

            stop_playback = False
            print("Playback completed")
            self.request.sendall(b'complete')

        elif self.data == 'pause':
            print("Pausing playback")

        elif self.data == 'stop':
            print("Stopping playback")
            stop_playback = True

        else:
            print("Invalid command received")

def play_audio(sound):
    sound.play()
    while pygame.mixer.get_busy():
        if stop_playback:
            sound.stop()
            break
        time.sleep(0.1)

def play_video(video_file):
    command = f"sudo video-viewer {video_file} --led-slowdown-gpio=2 --led-rows=32 --led-cols=64 --led-chain=4 --led-parallel=2 --led-pixel-mapper=V-mapper:Z -f"
    print(command)
    subprocess.run(command, shell=True)

def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')

    host = config['MediaPlayer']['IP']
    port = int(config['MediaPlayer']['Port'])
    print(port, host)
    
    pygame.mixer.init(frequency=44100, size=-16, channels=2)
    print("Player is ready.")

    server = socketserver.ThreadingTCPServer((host, port), PlayerHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
