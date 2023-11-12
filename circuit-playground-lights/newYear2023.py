import array
import math
import board
import neopixel
import audiobusio
import time
from adafruit_circuitplayground import cp

NUM_PIXELS = 50
WHITE = (10, 10, 10)
MIDDLE = (3, 3, 8)
BLUE = (0, 0, 10)

pixels = neopixel.NeoPixel(board.A1, NUM_PIXELS)

def fade_to_white(light):
    r = 0
    g = 0
    b = 20
    while (r < 20 and g < 20):
        r = r + 2
        g = g + 2
        pixels[light] = (r, g, b)
        time.sleep(0.05)
    
def fade_to_blue(light):
    r = 20
    g = 20
    b = 20
    while (r > 0 and g > 0):
        r = r - 2
        g = g - 2
        pixels[light] = (r, g, b)
        time.sleep(0.05)

pixels.fill(BLUE)
pixels.show()
while True:
    for i in range(NUM_PIXELS):
        fade_to_white(i)
        
    for i in range(NUM_PIXELS):
        fade_to_blue(i)

    pixels.show()
    time.sleep(10)