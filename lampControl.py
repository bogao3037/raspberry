import RPi.GPIO as GPIO
import time

lamp = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(lamp, GPIO.OUT)



while True:
    time.sleep(1)
    GPIO.output(lamp, True)
    time.sleep(1)
    GPIO.output(lamp,False)
