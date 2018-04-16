#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
# http://RasPi.tv/
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi
#-gpio-part-3
import RPi.GPIO as GPIO
import ADC0832 as ADC
import subprocess
import Adafruit_CharLCD as LCD
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lcd = LCD.Adafruit_CharLCDPlate()
selectADC = False
while True:
        IPaddr = subprocess.check_output(['hostname ', ' -I'])
        if len(IPaddr) > 8:
                break
        else:
                time.sleep(2)
Name = subprocess.check_output(['hostname']).strip()
displayText = IPaddr + Name


def getvoltage():
    stepspervolt = 3.3 / 255
    ADCvalue = ADC.getResult()
    ADCvoltage = ADCvalue * stepspervolt
    Displaystring = "ADC voltage:\n %3.3f" % ADCvoltage
    return Displaystring


def subtractvoltage(getvoltage):
    return Displaystring


def getIP():
    return displayText


def my_callbackADC(channel):
    global selectADC
    selectADC = True


def my_callbackIP(channel):
    global selectADC
    selectADC = False


# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callbackADC, bouncetime=300)

# when a falling edge is detected on port 23, regardless of whatever
# else is happening in the program, the function my_callback2 will be run
# 'bouncetime=300' includes the bounce control written into interrupts2a.py
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callbackIP, bouncetime=300)

olddisplay = None

try:
    while True:
        if selectADC:
            display = getvoltage()
        else:
            display = getIP()
        if display == olddisplay:
            pass
        else:
            lcd.clear()
            lcd.message(display)
            olddisplay = display
        time.sleep(0.4)


except KeyboardInterrupt:
    GPIO.cleanup()    # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit