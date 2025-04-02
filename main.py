from pynput import keyboard
import simpleaudio as sa
import os

# Load sound (replace with your .wav file name)
sound_path = os.path.join(os.path.dirname(__file__), "key.wav")
sound = sa.WaveObject.from_wave_file(sound_path)

def on_press(key):
    try:
        sound.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

    if key == keyboard.Key.esc:
        print("Exiting...")
        return False

print("Mechanical keyboard sim running. Press ESC to quit.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
