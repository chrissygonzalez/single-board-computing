# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Christmas 2022 version

"""This example uses the sound sensor, located next to the picture of the ear on your board, to
light up the NeoPixels as a sound meter. Try talking to your Circuit Playground or clapping, etc,
to see the NeoPixels light up!"""
import array
import math
import board
import neopixel
import audiobusio
import time
from adafruit_circuitplayground import cp

NUM_PIXELS = 20

pixels = neopixel.NeoPixel(board.A1, NUM_PIXELS)
pixels.brightness = 0.3


def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / (input_max - input_min)
    return output_min + math.pow(normalized_input_value, 0.630957) * (
        output_max - output_min
    )


def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return math.sqrt(
        sum(float(sample - minbuf) * (sample - minbuf) for sample in values)
        / len(values)
    )

def in_range(num, num_range):
    if num < num_range and num >= 0:
        return True
    else:
        return False

mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16
)

samples = array.array("H", [0] * 160)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + NUM_PIXELS

# Lower number means more sensitive - more LEDs will light up with less sound.
sensitivity = 120
input_ceiling = input_floor + sensitivity

peak = 0
GREEN = (0, 50, 0)
RED = (25, 0, 0)

red_value = 0
green_value = 50
blue_value = 0
turning_red = True
increment = 5
midpoint = math.floor(NUM_PIXELS / 2)



pixels.fill(GREEN)
while True:
    mic.record(samples, len(samples))
#    magnitude = normalized_rms(samples)
#    print("Here!")
#    print((magnitude,))

#    c = log_scale(
#        constrain(magnitude, input_floor, input_ceiling),
#        input_floor,
#        input_ceiling,
#        0,
#        NUM_PIXELS,
#    )

    for i in range(midpoint + 2):
        pixels.fill(GREEN)

        while red_value < 50:
            if in_range(midpoint - i, NUM_PIXELS):
                pixels[midpoint - i] = (red_value, green_value, blue_value)
            if in_range(midpoint - i - 2, NUM_PIXELS):
                pixels[midpoint - i - 2] = (red_value, green_value, blue_value)
            if in_range(midpoint + i, NUM_PIXELS):
                pixels[midpoint + i] = (red_value, green_value, blue_value)
            if in_range(midpoint + i + 2, NUM_PIXELS):
                pixels[midpoint + i + 2] = (red_value, green_value, blue_value)
            red_value = red_value + 1
            green_value = green_value - 1

        red_value = 0
        green_value = 50
        time.sleep(0.5)
        pixels.show()

    #time.sleep(0.1)
 #       if i < c:
 #           pixels[i] = RED
 #       if c >= peak:
 #           peak = min(c, NUM_PIXELS - 1)
 #       elif peak > 0:
 #           peak = peak - 1
 #       if peak > 0:
 #           pixels[int(peak)] = RED
