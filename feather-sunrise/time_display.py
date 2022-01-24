import time
import math

zero = [2, 3, 4, 5, 6, 10, 14, 18, 19, 20, 21, 22]
one = [10, 11, 12, 13, 14, 18]
two = [2, 3, 4, 6, 10, 12, 14, 18, 20, 21, 22]
three = [2, 3, 4, 5, 6, 10, 12, 14, 18, 20, 22]
four = [2, 3, 4, 5, 6, 12, 18, 19, 20]
five = [2, 4, 5, 6, 10, 12, 14, 18, 19, 20, 22]
six = [2, 4, 5, 6, 10, 12, 14, 18, 19, 20, 21, 22]
seven = [2, 3, 4, 5, 6, 10, 18]
eight = [2, 3, 4, 5, 6, 10, 12, 14, 18, 19, 20, 21, 22]
nine = [2, 3, 4, 5, 6, 10, 12, 14, 18, 19, 20, 22]
colon = [11, 13]

digit_map = {
    0: zero,
    1: one,
    2: two,
    3: three,
    4: four,
    5: five,
    6: six,
    7: seven,
    8: eight,
    9: nine,
}


def shift_pixels(pixels, shift, back = True):
    shifted_pixels = []
    for pixel in pixels:
        if back:
            shifted_pixels.append(pixel - shift)
        else:
            shifted_pixels.append(pixel + shift)
    return shifted_pixels


def get_digits(num):
    if num < 10:
        tens = 0
        ones = num
    else:
        tens = math.floor(num / 10)
        ones = num % 10
    return [tens, ones]


def get_time_digits(hour, minute):
    hour_digits = get_digits(hour)
    minute_digits = get_digits(minute)
    return hour_digits + minute_digits


def get_time_pixels_to_show(hour, minute, shift):
    #convert time to individual digits
    digits = get_time_digits(hour, minute)

    #get pixels to show for each digit, shift each 4 cols per position
    digits0 = shift_pixels(digit_map[digits[0]], shift * 0)
    digits1 = shift_pixels(digit_map[digits[1]], shift * 4)
    digits2 = shift_pixels(colon, shift * 8)
    digits3 = shift_pixels(digit_map[digits[2]], shift * 12)
    digits4 = shift_pixels(digit_map[digits[3]], shift * 16)

    #make one big array of pixels to show all digits
    all_pixels_to_show = digits0 + digits1 + digits2 + digits3 + digits4

    return all_pixels_to_show


def show_time(hour, minute, shift, pixels, color):
    local_shift = 0
    pixels_to_show = get_time_pixels_to_show(hour, minute, shift)
    while local_shift < 200:
        shifted_pixels = shift_pixels(pixels_to_show, local_shift, False)
        show_pixels(pixels, shifted_pixels, color)
        local_shift = local_shift + shift
        time.sleep(0.2)
        

def show_pixels(pixels, pixels_to_show, color):
    # look for faster way to reset and show pixels?
    # it's kind of blinky as it animates
    for led in range(32):
        pixels[led] = (0, 0, 0)
    for pixel in pixels_to_show:
        if pixel < len(pixels) and pixel > 0:
            pixels[pixel] = color
    pixels.show()