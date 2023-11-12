# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Halloween 2020 version of this program, as of Nov 5

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

pixels = neopixel.NeoPixel(board.A1, 50)


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


mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16
)

samples = array.array("H", [0] * 160)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 50

# Lower number means more sensitive - more LEDs will light up with less sound.
sensitivity = 80
input_ceiling = input_floor + sensitivity

peak = 0
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print("Here!")
    print((magnitude,))

    c = log_scale(
        constrain(magnitude, input_floor, input_ceiling),
        input_floor,
        input_ceiling,
        0,
        50,
    )

    pixels.fill((10, 0, 20))
    for i in range(50):
        if i < c:
            #pixels[i] = (i * (255 // 10), 50, 0)
            pixels[i] = (55, 10, 0)
        if c >= peak:
            peak = min(c, 50 - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            pixels[int(peak)] = (55, 10, 0)
    pixels.show()
    time.sleep(0.05)