@echo off
echo Setting up Keyboard Sound Task...
schtasks /Create /SC ONLOGON /TN "KeyboardSound" /TR "'C:\Python310\python.exe' 'C:\Users\Owner\Desktop\Projects\thwak\giga.py'" /RL HIGHEST /F
echo Task created successfully. The script will run when you log in.
pause
