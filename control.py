#!/usr/bin/python
#This is a demo 

import RPi.GPIO as GPIO
import time
import smbus
import time
from Tkinter import *

root = Tk()
root.title("Montreal LowTech Consulting")
root.geometry("500x500")
LampGPIO = 18
MotionSensor = 17
varTemp = StringVar()
varHumidity = StringVar()
varMotion = StringVar()
varMotion.set("No Detect")
motionPreState = False
motionCurState = False  

def ControlLamp():
    GPIO.output(LampGPIO, True)
    time.sleep(0.1)
    GPIO.output(LampGPIO,False)

def TempHumidityUpdate(label):    
    # Get I2C bus
    bus = smbus.SMBus(1)
        # SI7006_A20 address, 0x40(64)
    #		0xF5(245)	Select Relative Humidity NO HOLD MASTER mode
    bus.write_byte(0x40, 0xF5)
    time.sleep(0.5)
    # SI7006_A20 address, 0x40(64)
    # Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)
    
    # Convert the data
    humidity = (125.0 * (data0 * 256.0 + data1) / 65536.0) - 6.0
    
    # SI7006_A20 address, 0x40(64) 
    #		0xF3(243)	Select temperature NO HOLD MASTER mode
    bus.write_byte(0x40, 0xF3)
    
    time.sleep(0.5)
    
    # SI7006_A20 address, 0x40(64)
    # Read data back, 2 bytes, Temperature MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)
    
    # Convert the data
    cTemp = (175.72 * (data0 * 256.0 + data1) / 65536.0) - 46.85
    fTemp = cTemp * 1.8 + 32
    varTemp.set("Temperature: %.2f C" %cTemp)
    varHumidity.set("Humidity: %.2f" %humidity)
    label.after(1000, TempHumidityUpdate,(label))
        
def MotionUpdate(label):    
    global motionCurState
    motionPreState = motionCurState
    motionCurState = GPIO.input(MotionSensor)
    if motionCurState != motionPreState:
        new_state = "Motion Detected" if motionCurState else "No Detect"
        varMotion.set(new_state)
            #print("GPIO pin %s is %s" % (MotionSensor, new_state))
    label.after(1000, MotionUpdate,(label))           
        
if __name__ == '__main__':        
 #Motion Sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotionSensor, GPIO.IN, GPIO.PUD_DOWN)   

    labelMotion = Label(root, textvariable = varMotion,fg="green",height=2)
    labelMotion.pack(side=TOP)    
    labelMotion.config(font=16)
    MotionUpdate(labelMotion)

    labelTemp = Label(root, textvariable = varTemp,fg="red",height=2)
    labelTemp.pack(side=TOP)
    labelTemp.config(font=16)
	
    labelHumidity = Label(root, textvariable = varHumidity,fg="blue",height=2)
    labelHumidity.pack(side=TOP)
    labelHumidity.config(font=16)
	
    TempHumidityUpdate(labelTemp)
    

	
   
    

    


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LampGPIO, GPIO.OUT)
    
    button = Button(root, text='ON/OFF', width=25,height = 10, command=ControlLamp)
    button.config(font=16)
    button.pack(side=BOTTOM)
    root.mainloop()   
    