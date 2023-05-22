import socketserver
import configparser
import threading
import time
import simpleaudio as sa
import subprocess
import signal
import os

config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
config = configparser.ConfigParser()
config.read(config_path)
red_wav = config['MediaPlayer']['red_wav']
blue_wav = config['MediaPlayer']['blue_wav']
red_video = config['MediaPlayer']['red_video']
blue_video = config['MediaPlayer']['blue_video']
loaded = "red"
audio_playback = None
video_viewer_process = None
audio_playback_complete = threading.Event()

# Load audio files
red_sound = sa.WaveObject.from_wave_file(red_wav)
blue_sound = sa.WaveObject.from_wave_file(blue_wav)

class PlayerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global loaded, audio_playback, video_viewer_process
        self.data = self.request.recv(1024).strip().decode('utf-8')

        if self.data.startswith('load'):
            track_id = self.data.split(' ')[1]
            print("Loading track with ID:", track_id)
            loaded = track_id

        elif self.data == 'play':
            print("Starting playback", loaded)
            if loaded == "red":
                sound = red_sound
                video_file = red_video
            else:
                sound = blue_sound
                video_file = blue_video

            audio_playback_complete.clear()
            audio_playback = play_audio(sound)
            watch_playback_thread = threading.Thread(target=watch_playback, args=(audio_playback,))
            watch_playback_thread.start()

            # Start the video playback in the main thread
            video_viewer_process = play_video(video_file)

            audio_playback_complete.wait()
            if video_viewer_process is not None:
                stop_video_viewer(video_viewer_process)
            print("Playback completed")
            self.request.sendall(b'complete')

        elif self.data == 'stop':
            print("Stopping playback")
            if audio_playback is not None:
                audio_playback.stop()
            if video_viewer_process is not None:
                stop_video_viewer(video_viewer_process)

        else:
            print("Invalid command received")

def play_audio(sound):
    return sound.play()

def watch_playback(play_obj):
    while play_obj.is_playing():
        time.sleep(0.1)
    audio_playback_complete.set()

def play_video(video_file):
    # Start the video viewer process using subprocess.Popen
    command = f"sudo video-viewer {video_file} --led-slowdown-gpio=2 --led-rows=32 --led-cols=64 --led-chain=4 --led-parallel=2 --led-pixel-mapper=V-mapper:Z -f"
    return subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

def stop_video_viewer(process):
    # Stop the video viewer process using os.killpg and signal.SIGKILL
    os.killpg(os.getpgid(process.pid), signal.SIGKILL)

def main():
    host = config['MediaPlayer']['IP']
    port = int(config['MediaPlayer']['Port'])
    print(port, host)

    print("Player is ready.")

    server = socketserver.ThreadingTCPServer((host, port), PlayerHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
