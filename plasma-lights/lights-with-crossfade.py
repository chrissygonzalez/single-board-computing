import board
import time
import neopixel

NUM_LEDS = 50
BRIGHTNESS = 0.1

LIGHT_PINK = (220, 59, 136)
DARK_PINK = (240, 35, 0)
GREEN = (0, 245, 0)
RED = (245, 0, 0)
ORANGE = (220, 0, 50)
PURPLE = (100, 0, 100)

led_strip = neopixel.NeoPixel(board.DATA, NUM_LEDS, brightness=BRIGHTNESS, auto_write=True)
led_strip.show()

chase_pixel = 0

#def _map(x, in_min, in_max, out_min, out_max):
#    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def color_step(color_value, diff, start, num_steps):
    return int(color_value * diff / num_steps + start)

def cross_fade(pixel_list, diffs, starts, num_steps, delay):
    for color_value in range(num_steps):
        red = color_step(color_value, diffs[0], starts[0], num_steps)
        blue = color_step(color_value, diffs[1], starts[1], num_steps)
        green = color_step(color_value, diffs[2], starts[2], num_steps)
        for pixel in pixel_list:
            led_strip[pixel] = (red, green, blue)
        time.sleep(delay)

def chase_lights(main_color, chase_color, chunk = 4):
    global chase_pixel
    pixels_to_change = []

    start_red = main_color[0]
    start_blue = main_color[1]
    start_green = main_color[2]
    starts = (start_red, start_blue, start_green)

    end_red = chase_color[0]
    end_blue = chase_color[1]
    end_green = chase_color[2]

    red_diff = end_red - start_red
    blue_diff = end_blue - start_blue
    green_diff = end_green - start_green
    diffs = (red_diff, blue_diff, green_diff)

    for i in range(NUM_LEDS):
        led_strip[i] = main_color

    for i in range(NUM_LEDS):
        if i == chase_pixel or (i - chase_pixel) % chunk == 0:
            pixels_to_change.append(i)

    cross_fade(pixels_to_change, diffs, starts, 5, 0.05)

    if chase_pixel < chunk - 1:
        chase_pixel += 1
    else:
        chase_pixel = 0


while True:
    chase_lights(LIGHT_PINK, DARK_PINK, 3)
    time.sleep(0.5)
