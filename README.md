# Python Keylogger
The keylooger takes a screenshot and saves it to a directory every 30 seconds using the pyautogui module. The function schedules the next screenshot using the threading.Timer class, just like before. at caputures every keyskrokes and saves them to a text file, and later send the txt file to any email address you specify.

# Installation Instruction
First, install the required modules:
1. PIL (pillow)
2. pynput

```
pip3 install pillow
```
```
pip3 install pynput
```

# Usage
```
python keycap.py
```

# Convert it to exe to run on any windows machine
```
pyinstaller --onefile keycap.py
```
