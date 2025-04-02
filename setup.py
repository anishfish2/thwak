from setuptools import setup

APP = ['main.py']
DATA_FILES = ['key.wav']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pynput', 'simpleaudio'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
