import winsound
import time
import threading
import ctypes
from ctypes import wintypes
import os
import sys

# Windows constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
HC_ACTION = 0

# Global variables
SOUND_PLAYING = False
SOUND_LOCK = threading.Lock()

def get_executable_dir():
    """Get the directory where the executable or script is located"""
    if getattr(sys, 'frozen', False):
        # Running as executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

# Get sound file path
sound_file = os.path.join(get_executable_dir(), "key.wav")

# Verify sound file exists
if not os.path.exists(sound_file):
    print(f"ERROR: Sound file not found at: {sound_file}")
    print("Please place a file named 'key.wav' in the same directory as this program.")
    time.sleep(5)
    sys.exit(1)
else:
    print(f"Found sound file: {sound_file}")

def play_sound_thread():
    """Play sound in a separate thread to avoid blocking"""
    global SOUND_PLAYING
    
    with SOUND_LOCK:
        if SOUND_PLAYING:
            return
        SOUND_PLAYING = True
    
    try:
        # Use Windows built-in sound playing (no pygame needed)
        winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"Error playing sound: {e}")
    
    # Small delay to prevent sound overlap
    time.sleep(0.05)
    
    with SOUND_LOCK:
        SOUND_PLAYING = False

def low_level_keyboard_handler(nCode, wParam, lParam):
    """Keyboard hook callback function"""
    if nCode == HC_ACTION and wParam == WM_KEYDOWN:
        # Start sound in a separate thread to prevent UI blocking
        threading.Thread(target=play_sound_thread, daemon=True).start()
    
    # Call the next hook in the chain
    return ctypes.windll.user32.CallNextHookEx(0, nCode, wParam, lParam)

def main():
    # Define C function type for the hook procedure
    HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
    
    # Convert the Python callback function to a C function pointer
    pointer = HOOKPROC(low_level_keyboard_handler)
    
    # Get module handle
    hinst = ctypes.windll.kernel32.GetModuleHandleW(None)
    
    # Set the keyboard hook
    hook_id = ctypes.windll.user32.SetWindowsHookExW(
        WH_KEYBOARD_LL,
        pointer,
        hinst,
        0
    )
    
    if not hook_id:
        print("Failed to set keyboard hook!")
        return
    
    print("Keyboard Sound Application Running")
    print("Every key press will trigger a sound")
    print("This window can be minimized")
    print("Press Ctrl+C in this window to exit")
    
    # Message loop to keep the hook active
    msg = wintypes.MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting application...")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)