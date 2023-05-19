import pygame

# Initialize Pygame
pygame.init()

# Specify the path to the WAV file
wav_file = "/home/pi/teledisko/media-player/sound/red230519.wav"

# Set the mixer frequency and size
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Load the WAV file
sound = pygame.mixer.Sound(wav_file)

# Play the WAV file
sound.play()

# Wait until the sound finishes playing
while pygame.mixer.get_busy():
    pass

# Clean up the Pygame mixer
pygame.mixer.quit()
