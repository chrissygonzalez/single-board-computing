zero = [1, 2, 3, 4, 5, 6, 7, 9, 15, 17, 23, 25, 26, 27, 28, 29, 30, 31]
one = [9, 10, 11, 12, 13, 14, 15, 17]
two = [1, 2, 3, 4, 7, 9, 12, 15, 17, 20, 23, 25, 28, 29, 30, 31]
three = [1, 2, 3, 4, 5, 6, 7, 9, 12, 15, 17, 20, 23, 25, 28, 31]
four = [1, 2, 3, 4, 5, 6, 7, 12, 20, 25, 26, 27, 28]
five = [1, 4, 5, 6, 7, 9, 12, 15, 17, 20, 23, 25, 26, 27, 28, 31]
six = [1, 4, 5, 6, 7, 9, 12, 15, 17, 20, 23, 25, 26, 27, 28, 29, 30, 31]
seven = [1, 2, 3, 4, 5, 6, 7, 9, 17, 25]
eight = [1, 2, 3, 4, 5, 6, 7, 9, 12, 15, 17, 20, 23, 25, 26, 27, 28, 29, 30, 31]
nine = [1, 2, 3, 4, 5, 6, 7, 9, 12, 15, 17, 20, 23, 25, 26, 27, 28, 31]
colon = [9, 10, 13, 14, 17, 18, 21, 22]

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
    pixels_to_show = get_time_pixels_to_show(hour, minute, shift)
    pixels2 = shift_pixels(pixels_to_show, shift, False)
    pixels3 = shift_pixels(pixels_to_show, (shift * 2), False)
    print(pixels2)
    show_pixels(pixels, pixels3, color)
    
def show_pixels(pixels, pixels_to_show, color):
    for pixel in pixels_to_show:
        if pixel < len(pixels) and pixel > 0:
            pixels[pixel] = color
    pixels.show()
