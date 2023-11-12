import array
import math
import board
import neopixel
import audiobusio
import time
import random
from adafruit_circuitplayground import cp

NUM_PIXELS = 20
WHITE = (10, 10, 10)
MIDDLE = (3, 3, 8)
BLUE = (0, 0, 10)
PINK = (30, 10, 10)
RED = (30, 0, 0)

pixels = neopixel.NeoPixel(board.A1, NUM_PIXELS)

#---- MIC FUNCTIONS
def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(sum_of_samples / len(values))


mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)
mic.record(samples, len(samples))


#---- LIGHT FUNCTIONS
def createList(r1, r2):
    return [item for item in range(r1, r2+1)]

pinkList = createList(0, NUM_PIXELS - 1)

redList = []

def addToRed(r1, r2):
    #print("length of pinkList: ", len(pinkList))
    if len(pinkList) > 0:
        index = random.randint(r1, r2)
        while index >= len(pinkList):
            index = random.randint(r1, r2)
        #print(index)
        redList.append(pinkList[index])
        pinkList.pop(index)

def addToPink():
    item = redList.pop()
    pinkList.append(item)

pixels.fill(PINK)
pixels.show()
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples) / 10
    if magnitude > NUM_PIXELS - 1:
        magnitude = NUM_PIXELS - 1

    while len(redList) < magnitude:
        addToRed(0, len(pinkList))

    while len(redList) > magnitude:
        addToPink()

    for x in redList:
        pixels[x] = RED
        pixels.show()
        
    for x in pinkList:
        pixels[x] = PINK
        pixels.show()

    print(((math.floor(magnitude)),))


    pixels.show()
    time.sleep(0.01)

#OLDER
# import array
# import math
# import board
# import neopixel
# import audiobusio
# import time
# import random
# from adafruit_circuitplayground import cp

# NUM_PIXELS = 20
# WHITE = (10, 10, 10)
# MIDDLE = (3, 3, 8)
# BLUE = (0, 0, 10)
# PINK = (30, 10, 10)
# RED = (30, 0, 0)

# pixels = neopixel.NeoPixel(board.A1, NUM_PIXELS)

# #---- MIC FUNCTIONS
# def mean(values):
#     return sum(values) / len(values)


# def normalized_rms(values):
#     minbuf = int(mean(values))
#     sum_of_samples = sum(
#         float(sample - minbuf) * (sample - minbuf)
#         for sample in values
#     )

#     return math.sqrt(sum_of_samples / len(values))


# mic = audiobusio.PDMIn(
#     board.MICROPHONE_CLOCK,
#     board.MICROPHONE_DATA,
#     sample_rate=16000,
#     bit_depth=16
# )
# samples = array.array('H', [0] * 160)
# mic.record(samples, len(samples))


# #---- LIGHT FUNCTIONS
# def createList(r1, r2):
#     return [item for item in range(r1, r2+1)]

# pinkList = createList(0, NUM_PIXELS - 1)

# redList = []

# def changeIndexToRed(r1, r2):
#     print("length of pinkList: ", len(pinkList))
#     if len(pinkList) > 0:
#         index = random.randint(r1, r2)
#         while index >= len(pinkList):
#             index = random.randint(r1, r2)
#         print(index)
#         redList.append(pinkList[index])
#         pinkList.pop(index)

# pixels.fill(PINK)
# pixels.show()
# while True:
#     mic.record(samples, len(samples))
#     magnitude = normalized_rms(samples) / 10
#     if magnitude > NUM_PIXELS:
#         magnitude = NUM_PIXELS - 1


#     changeIndexToRed(0, len(pinkList))

#     for x in redList:
#         pixels[x] = RED
#         pixels.show()

#     print(((math.floor(magnitude)),))


#     pixels.show()
#     time.sleep(1)
