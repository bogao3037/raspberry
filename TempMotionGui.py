# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7006-A20
# This code is designed to work with the SI7006-A20_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SI7006-A20_I2CS#tabs-0-product_tabset-2
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
motionPreState = False
motionCurState = False  

def ControlLamp():
    GPIO.output(LampGPIO, True)
    time.sleep(1)
    GPIO.output(LampGPIO,False)

def TempHumidityUpdate(label):    
    # Get I2C bus
    bus = smbus.SMBus(1)
        # SI7006_A20 address, 0x40(64)
    #		0xF5(245)	Select Relative Humidity NO HOLD MASTER mode
    bus.write_byte(0x40, 0xF5)
    time.sleep(0.2)
    # SI7006_A20 address, 0x40(64)
    # Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)
    
    # Convert the data
    humidity = (125.0 * (data0 * 256.0 + data1) / 65536.0) - 6.0
    
    # SI7006_A20 address, 0x40(64) 
    #		0xF3(243)	Select temperature NO HOLD MASTER mode
    bus.write_byte(0x40, 0xF3)
    
    time.sleep(0.2)
    
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
        new_state = "HIGH" if motionCurState else "LOW"
        varMotion.set("GPIO pin %s is %s" % (MotionSensor, new_state))
            #print("GPIO pin %s is %s" % (MotionSensor, new_state))
    label.after(1000, MotionUpdate,(label))           
        
if __name__ == '__main__':        



    labelTemp = Label(root, textvariable = varTemp)
    labelTemp.pack(side=TOP)
    TempHumidityUpdate(labelTemp)
    
    labelHumidity = Label(root, textvariable = varHumidity)
    labelHumidity.pack(side=TOP)
    
    #Motion Sensor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotionSensor, GPIO.IN, GPIO.PUD_DOWN)   
    
    labelMotion = Label(root, textvariable = varMotion)
    labelMotion.pack(side=TOP)    
    MotionUpdate(labelMotion)
    


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LampGPIO, GPIO.OUT)
    
    button = Button(root, text='ON/OFF', width=25, command=ControlLamp)
    button.pack()
    root.mainloop()   
    