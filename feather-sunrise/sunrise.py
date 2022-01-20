import random
import time
import board
from analogio import AnalogIn
import neopixel
import adafruit_ds3231

i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

#set_time = time.struct_time((2022, 1, 9, 18, 14, 00, 6, 9, 0))
#print("Setting time to:", set_time)
#rtc.datetime = set_time

RED = (100, 0, 0)
BRIGHT_RED = (255, 0, 0)
ORANGE = (225, 100, 0)
YELLOW = (255, 150, 0)
WHITE = (255, 200, 150)
BLACK = (0, 0, 0)

pixels = neopixel.NeoPixel(board.D6, 32, brightness=0.02)    # Feather wiring!
boardPixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2


def showColor(led, color, delay):
    pixels[led] = color
    pixels.show()
    time.sleep(delay)

def showLights(color, delay):
    #pixels.brightness = 0.2
    leds = [x for x in range(32)]
    #print(leds)

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
    time.sleep(60)
    pixels.brightness = 0.4
    time.sleep(60)
    pixels.brightness = 0.5
    #time.sleep(600)
    #showLights(BLACK, 0)

while True:
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
    if current.tm_hour == 3 and current.tm_min == 20:
        print('starting the sunrise')
        sunrise()
