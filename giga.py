import winsound
import time
import threading
import ctypes
from ctypes import wintypes
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyboard_sound.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log startup information
logging.info("Application starting")

# Windows constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
HC_ACTION = 0

# Global variables
SOUND_PLAYING = False
SOUND_LOCK = threading.Lock()

def get_script_dir():
    """Get the directory of the script"""
    return os.path.dirname(os.path.abspath(__file__))

# Sound file path
sound_file = os.path.join(get_script_dir(), "key.wav")

# Verify sound file exists
if not os.path.exists(sound_file):
    logging.error(f"Sound file not found: {sound_file}")
    print(f"ERROR: Sound file not found at: {sound_file}")
    print("Please place a file named 'key.wav' in the same directory as this script.")
    time.sleep(5)
    sys.exit(1)

logging.info(f"Found sound file: {sound_file}")
print(f"Found sound file: {sound_file}")

def play_sound():
    """Play sound when triggered"""
    global SOUND_PLAYING
    
    with SOUND_LOCK:
        if SOUND_PLAYING:
            return
        SOUND_PLAYING = True
    
    try:
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    except Exception as e:
        logging.error(f"Error playing sound: {e}")
        print(f"Error playing sound: {e}")
    
    with SOUND_LOCK:
        SOUND_PLAYING = False

def low_level_keyboard_handler(nCode, wParam, lParam):
    """Keyboard hook callback function"""
    if nCode == HC_ACTION and wParam == WM_KEYDOWN:
        # Start sound in a separate thread to prevent UI blocking
        threading.Thread(target=play_sound, daemon=True).start()
    
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
        logging.error("Failed to set keyboard hook!")
        print("Failed to set keyboard hook! Please run this script as Administrator.")
        time.sleep(5)
        return
    
    logging.info("Keyboard hook set successfully")
    print("Keyboard Sound Application Running")
    print("Every key press will trigger a sound")
    print("This window can be minimized (but not closed)")
    print("Press Ctrl+C in this window to exit")
    
    # Message loop to keep the hook active
    msg = wintypes.MSG()
    while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

# Create the task scheduler setup script
def create_task_scheduler_script():
    bat_path = os.path.join(get_script_dir(), "setup_keyboard_sound_task.bat")
    
    python_path = sys.executable
    script_path = os.path.abspath(__file__)
    
    batch_content = f"""@echo off
echo Setting up Keyboard Sound Task...
schtasks /Create /SC ONLOGON /TN "KeyboardSound" /TR "'{python_path}' '{script_path}'" /RL HIGHEST /F
echo Task created successfully. The script will run when you log in.
pause
"""
    
    with open(bat_path, "w") as f:
        f.write(batch_content)
    
    print(f"Created task scheduler setup script: {bat_path}")
    print("Run this script as Administrator to set up automatic startup.")

if __name__ == "__main__":
    try:
        # Create the setup script if it doesn't exist
        setup_script = os.path.join(get_script_dir(), "setup_keyboard_sound_task.bat")
        if not os.path.exists(setup_script):
            create_task_scheduler_script()
        
        # Run the main application
        main()
    except KeyboardInterrupt:
        logging.info("Application stopped by user")
        print("Exiting application...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Error: {e}")
        time.sleep(5)