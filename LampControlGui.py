from Tkinter import *
import RPi.GPIO as GPIO
import time

class HelloButton(Button):
    def __init__(self, parent=None, **config):         # add callback method
    
        Button.__init__(self, parent, **config)        # and pack myself
        self.lamp = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.lamp, GPIO.OUT)

        self.pack()                                    # could config style too
        self.config(command=self.callback)

    def callback(self):                                # default press action
        #print('Goodbye world...')                      # replace in subclasses
        GPIO.output(self.lamp, True)
        #time.sleep(1)
        time.sleep(1)
        GPIO.output(self.lamp,False)

if __name__ == '__main__':
    HelloButton(text='ON/OFF').mainloop()