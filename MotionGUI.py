import RPi.GPIO as GPIO
import time
from Tkinter import *

sensor = 17
root = Tk()
var = StringVar()
l = Label(root, textvariable = var)
l.pack()

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

while True:
    time.sleep(0.2)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        var.set("GPIO pin %s is %s" % (sensor, new_state))
        print("GPIO pin %s is %s" % (sensor, new_state))
    root.update_idletasks()