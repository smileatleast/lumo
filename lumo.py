'''
SMART LAMP v2
KGARMIRE 
6.19.2016
'''

#---initialize---
nLED = 64

import random
from time import sleep
from functools import partial
from bibliopixel.led import LEDStrip
from bibliopixel.drivers.LPD8806 import *
import bibliopixel.colors as Color

#create driver for nLED pixels
driver = DriverLPD8806(nLED, c_order = ChannelOrder.GRB)
led = LEDStrip(driver)
def turn_off():
    global led
    led.all_off();
    led.update();
    
#---set execs---
'''
combo = pattern + color
two-word phrase / mix-n-match
i.e. "odds white" -> turns all odd pixels white;
'''

#>functions
def goCombo(pattern, color):
    if pattern in _patterns.keys():
        pattern = _patterns[pattern]()
    for pixel in pattern:
        led.set(pixel, readColor(color))
    led.update();
        
def every(n, reversed=False):
    #subfunction - every n pixel
    z = []
    for i in range(nLED):
        if i%n == 0 and (not reversed):
            z.append(i)
        elif i%n != 0 and reversed:
            z.append(i)
    return z
    
def randomPixels(n):
    #subfunction - return n random pixels
    z = []
    count = 0;
    while(count < n):
        x = random.randrange(nLED)
        if x not in z:
            z.append(x)
            count += 1
    z.sort()
    return z
    
def hex(value):
    #subfunction - hexstring to rgb tuple
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    
def readColor(color):
    #subfunction - determines what format color is in and converts if required
    global _colors
    tc = type(color)
    if tc == tuple and len(color)==3:
        return color
    elif tc == str:
        if color[0] == "#":
            return hex(color)
        else:
            try:
                return _colors[color]
            except KeyError:
                return _colors["error"]
    else:
        return _colors["error"]
    
#>glossaries
_patterns = {
    "all"   : partial(every, 1),
    "odds"  : partial(every, 2, True),
    "odd"   : partial(every, 2, True),
    "evens" : partial(every, 2),
    "even"  : partial(every, 2),
    "third" : partial(every, 3),
    "fourth": partial(every, 4)
    }
    
_colors = {
    "error"     : (255, 89, 89),
    "bright"    : (255,255,255),
    "dim"       : (100,100,100),
    "white"     : (255,200,200),
    "red"       : (255,  0,  0),
    "orange"    : (255,132,  0),
    "yellow"    : (255,170,  0),
    "green"     : (  0,255,  0),
    "blue"      : (  0,  0,255),
    "indigo"    : ( 75,  0,130),
    "purple"    : (128,  0,128)
    }

#---set modes---
'''
mode = keyword + "mode"
predefined combo based on keyword
i.e. "submarine mode" -> turns all pixels red;
'''

#>functions
def goMode(keyword):
    try:
        _modes[keyword]()
    except KeyError:
        goCombo(every(10), "error")
    
def rainbow(n):
    global led, nLED, _colors
    rb = [_colors["red"], _colors["orange"], _colors["yellow"], _colors["green"], _colors["blue"], _colors["indigo"], _colors["purple"]]
    dv = n/len(rb)
    for i in range(n):
        try:
            c = rb[i/dv];
        except IndexError:
            c = rb[-1]
        led.set(i, c);
    led.update();
    
def starlight(n):
    z = randomPixels(n/3)
    goCombo(z, "white")

def koi():
    global led, _colors, nLED
    for i in range(nLED):
        if i < 10 or i >= nLED-10:
            led.set(i, _colors["white"])
        else:
            led.set(i, _colors["blue"])
    led.update()

#>glossaries
_modes = {
    "on"           : partial(goCombo, "all", "on"),
    "lamp"         : partial(goCombo, "third", "#cc7722"),
    "off"          : partial(turn_off),
    "submarine"    : partial(goCombo, "all", "red"),
    "starlight"    : partial(starlight, nLED),
    "rainbow"      : partial(rainbow, nLED),
    "koi"          : partial(koi)
    }

#---animation---

def test(t):
    global led, _colors, nLED
    i = 0
    while True:
	led.all_off()
        led.set(i, _colors["green"])
        led.update()
        i += 1;
        if (i == nLED):
            i = 0
        sleep(t)

    
#---reader---
def lumoRead(a, b="mode"):
    if (b == "mode"):
        goMode(a)
    else:
        goCombo(a, b)
