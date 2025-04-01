import pygame
import keyboard
import random
import os
import sys
import time

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize Pygame mixer for sound playing
pygame.mixer.init()

# Sound file path
sound_file = resource_path("key.wav")

# Verify sound file exists
if not os.path.exists(sound_file):
    print(f"ERROR: Sound file not found: {sound_file}")
    print("Please make sure key.wav is in the same directory as the executable.")
    time.sleep(5)
    sys.exit(1)

print("Keyboard sound application started!")
print(f"Using sound file: {sound_file}")

# Load sound
try:
    sound = pygame.mixer.Sound(sound_file)
except Exception as e:
    print(f"Error loading sound: {e}")
    time.sleep(5)
    sys.exit(1)

def play_sound(e):
    """Play sound on key press"""
    sound.play()

# Hook for all keyboard events
keyboard.on_press(play_sound)

print("Press Ctrl+Q to exit")

# Add a way to exit the program
keyboard.wait('ctrl+q')
print("Application stopped")