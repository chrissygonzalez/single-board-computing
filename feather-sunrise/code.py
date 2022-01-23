import random
import math
import time
import board
from analogio import AnalogIn
import neopixel
import adafruit_ds3231
import time_display

i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

pixels = neopixel.NeoPixel(board.D6, 32, brightness=0.02)    # Feather wiring!
boardPixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# SET RTC ONCE
#set_time = time.struct_time((2022, 1, 9, 18, 14, 00, 6, 9, 0))
#print("Setting time to:", set_time)
#rtc.datetime = set_time

RED = (100, 0, 0)
ORANGE = (225, 100, 0)
YELLOW = (255, 150, 0)
WHITE = (255, 200, 150)
BLACK = (0, 0, 0)
AQUA = (0, 75, 100)

SCROLL_SHIFT = 8
HOUR = 6
MINUTE = 0

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
    
def showColor(led, color, delay):
    pixels[led] = color
    pixels.show()
    time.sleep(delay)

def showLights(color, delay):
    leds = [x for x in range(32)]

    while len(leds) > 0:
        num = random.randrange(0, len(leds))
        showColor(leds[num], color, delay)
        del leds[num]

def sunrise():
    showLights(RED, 3)
    time.sleep(60)
    pixels.brightness = 0.03
    time.sleep(60)
    showLights(ORANGE, 2)
    showLights(YELLOW, 0.5)
    showLights(WHITE, 2)
    time.sleep(60)
    pixels.brightness = 0.05
    time.sleep(60)
    pixels.brightness = 0.1
    time.sleep(60)
    pixels.brightness = 0.2
    time.sleep(60)
    pixels.brightness = 0.3

#time_display.get_time_pixels_to_show(HOUR, MINUTE, SCROLL_SHIFT)
time_display.show_time(HOUR, MINUTE, SCROLL_SHIFT, pixels, AQUA)
while True:
    #time_display.show_time(time_display.colon, SCROLL_SHIFT, pixels, AQUA)
    battery_voltage = get_voltage(vbat_voltage)
    current = rtc.datetime
    pixels.show()
    if battery_voltage < 3.2:
        print("battery voltage is", battery_voltage)
        boardPixel.fill(RED)
        boardPixel.show()
    else:
        boardPixel.fill(BLACK)
        boardPixel.show()
    if current.tm_hour == HOUR and current.tm_min == MINUTE:
        print('starting the sunrise')
        sunrise()
