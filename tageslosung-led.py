#!/usr/bin/env python
import time
import sys
import random
import smbus
import os

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from datetime import datetime

from smbus2 import SMBus
from bme280 import BME280



bus = SMBus(2)
bme280 = BME280(i2c_dev=bus)


#if len(sys.argv) < 2:
 #   sys.exit("Require an image argument")
#else:
#    image_file = sys.argv[1]

#image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64 #32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.gpio_slowdown = 4
options.brightness = 25
#options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()

scroll = ""
heute = ""
losungstext = ""
lehrtext = ""
test = 0
direction = "up"

def cross(i):
    textColor1 = graphics.Color(i,i,i)
    # Cross vertical
    graphics.DrawLine(offscreen_canvas, 6, 2, 6, 17, textColor1)
    graphics.DrawLine(offscreen_canvas, 7, 2, 7, 17, textColor1)
    graphics.DrawLine(offscreen_canvas, 8, 2, 8, 17, textColor1)

    # Cross horizontal
    graphics.DrawLine(offscreen_canvas, 2, 6, 12, 6, textColor1)
    graphics.DrawLine(offscreen_canvas, 2, 7, 12, 7, textColor1)
    graphics.DrawLine(offscreen_canvas, 2, 8, 12, 8, textColor1)

    # Words
    graphics.DrawLine(offscreen_canvas, 11, 11, 13, 11, textColor1)
    graphics.DrawLine(offscreen_canvas, 11, 12, 13, 12, textColor1)

    graphics.DrawLine(offscreen_canvas, 15, 11, 18, 11, textColor1)
    graphics.DrawLine(offscreen_canvas, 15, 12, 18, 12, textColor1)


    graphics.DrawLine(offscreen_canvas, 11, 14, 15, 14, textColor1)
    graphics.DrawLine(offscreen_canvas, 11, 15, 15, 15, textColor1)

    graphics.DrawLine(offscreen_canvas, 18, 14, 17, 14, textColor1)
    graphics.DrawLine(offscreen_canvas, 18, 15, 17, 15, textColor1)


def vers(x1, i):
    global offscreen_canvas
    global heute
    global min
    global test
    global direction
 
    fake = matrix.CreateFrameCanvas()
    font_Losung = graphics.Font()
    #font_Losung.LoadFont("fonts/tom-thumb.bdf")
    font_Losung.LoadFont("fonts/4x6.bdf")
    
    font_Lehrtext = graphics.Font()
    font_Lehrtext.LoadFont("fonts/4x6.bdf")
 
    
    #if test == 0:
        #direction = "up"
    #elif test == 255:
        #direction = "down"
        
    #if direction == "up":
        #test = test + 1
    #elif direction == "down":
        #test = test - 1
    
    #z = 84 + test
    textColor = graphics.Color(235, 177, 52)#36,84,110
    
    pos = offscreen_canvas.width/3
    global losungstext
    global lehrtext
    x = ""
    heute = "" 
    aktuellesDatum = datetime.now()
    
    f = open("Losungen2021.txt", "r")
    jetzt = aktuellesDatum.strftime('%d.%m.%Y')
    if heute != jetzt:
        for x in f:
            #somestring = f.readline()
            if jetzt in x:
                x = x.upper()
                x = x.rstrip('\n')
                aktuell = x.split('\t')
                heute = aktuell[0]
                losungstext = aktuell[2] + ' ' + aktuell[1]
                lehrtext = aktuell[4] + ' ' + aktuell[3]

    #print("heute:\t\t" + heute)
    #print("Losung:\t\t" +losungstext)
    #print("Lehrtextt\t:" +lehrtext)
    #print("Jetzt:\t\t" + jetzt)
    f.close()
    
    if x1 <= 60:
        x = losungstext.split()
    elif x1 >= 61 and x1 <= 120:
        x = lehrtext.split()
    
    y = 0
    l = 0
    max_line_width = 48  # für den automatischen Zeilenumbruch

    #global scroll
 
    line = font_Losung.height + 6
    new = ''

    for element in x:
        len1 = graphics.DrawText(fake, font_Losung, 0, 0, textColor, new + element)
        if l >= 2:
            max_line_width = matrix.width

        if len1 < max_line_width:    
            new = new + element + ' '
        else:
            #print(new)
            if l <= 1: # dont override the logo (cross)
                graphics.DrawText(offscreen_canvas, font_Losung, matrix.height / 3, line, textColor, new)
            elif line <= 58: # dont override clock and temerature
                graphics.DrawText(offscreen_canvas, font_Losung, 2, line, textColor, new)
            #else:
                #scroll = scroll + new
                #print(scroll)

            line = line + font_Losung.height
            new = element + ' '
            l = l + 1 
        

        if y == len(x)-1 and line <= 58: # Buch und Vers abtrennen und align right
            #print(new)
            len1 = graphics.DrawText(fake, font_Lehrtext, 0, 0, textColor, new)
            graphics.DrawText(offscreen_canvas, font_Lehrtext, 64 - len1, line, textColor, new)
        
        y = y + 1
        
    
def temp(temperature):
    global offscreen_canvas
    font = graphics.Font()
    font.LoadFont("fonts/4x6.bdf")
    textColor = graphics.Color(255,255,255)
    
    #aktuellesDatum = datetime.now()
    #res = os.popen("vcgencmd measure_temp").readline()
    #temp = res.replace("temp=","")
    #temp = temp.replace("''C\n", "")
    graphics.DrawText(offscreen_canvas, font, 2, matrix.height - 1, textColor, temperature)


def notify(x):
    global offscreen_canvas
    f = open("/tmp/Nachrichten.txt", "r")
    z = f.read()
    f.close()
    
    font = graphics.Font()
    font.LoadFont("fonts/4x6.bdf")
    textColor = graphics.Color(255,255,0)



    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    #print('{:0.1f}°C {:05.1f}hPa {:05.1f}%'.format(temperature, pressure, humidity))
    #temp(temperature)
    
    if z == "0" or z == "":
        if x >= 1 and x <= 9:
            temp('{:0.1f}°C'.format(temperature))
        elif x >= 10 and x <= 18:
            temp('{:03.0f}hPa'.format(pressure))
        elif x >= 19 and x <= 27:
            temp('{:0.1f}%'.format(humidity))
        elif x > 27 and x <= 30:
            datum()
    else:
        graphics.DrawText(offscreen_canvas, font, 4, matrix.height - 1, textColor,  "-> " + z)


    
def datum():
    global offscreen_canvas

    fake = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("fonts/4x6.bdf")
    textColor = graphics.Color(255,255,255)
    
    aktuellesDatum = datetime.now()
    fake = matrix.CreateFrameCanvas()
    len1 = graphics.DrawText(fake, font, 0, 0, textColor, aktuellesDatum.strftime('%d.%b'))
    graphics.DrawText(offscreen_canvas, font, 3, matrix.height - 1, textColor, aktuellesDatum.strftime('%d.%b'))


def uhr():
    global offscreen_canvas

    fake = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("fonts/4x6.bdf")
    textColor = graphics.Color(255,255,255)
    
    aktuelleZeit = datetime.now()
    fake = matrix.CreateFrameCanvas()
    len1 = graphics.DrawText(fake, font, 0, 0, textColor, aktuelleZeit.strftime('%H:%M:%S'))
    graphics.DrawText(offscreen_canvas, font, 64 - 1 - len1, matrix.height - 1, textColor, aktuelleZeit.strftime('%H:%M:%S'))



def adjust_brightness():
    global offscreen_canvas
    #global v_new = random.randint(5, 100)
    #global v_old
    #x = random.randint(5, 100)
    v = 10;
    #y = 0
     
    #matrix.brightness = 10

    
    #for y in range(10, 100, 10):
        #matrix.brightness = y
        #time.sleep(1)
        #print(y)
        #y = y + 10

try:
    print("Losung LED is running - Press CTRL-C to stop.")
    x = 1
    x1 = 1
    i = 255
    s = ""
    while True:
        offscreen_canvas.Clear()
        cross(i)
        vers(x1, i)
        uhr()
        notify(x)
        #air()
        
        #adjust_brightness()
        #offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        #temp()

        x += 1
        if x == 30:
            x = 1
        
        if x1 == 120:
            x1 = 1
        x1 += 1
        
        # code um das Kreuz hell und dunkel über die Farbe zu machen
        #if i <= 50:
            #s = "up"
        #elif i >= 200:
            #s = "down"
            
        #if s == "up":
            #i = i + 10
        #elif s == "down":
            #i = i - 10
        # code ende hell/dunkel
        
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)
