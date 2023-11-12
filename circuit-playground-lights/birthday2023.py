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
BLACK = (0, 0, 0)

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
def getRandomColor():
    red = random.randint(0, 255)
    blue = random.randint(0, 255)
    green = random.randint(0, 255)
    return (red, green, blue)

def createList(r1, r2):
    return [item for item in range(r1, r2+1)]

darkList = createList(0, NUM_PIXELS - 1)

brightList = []

colorsList = createList(0, NUM_PIXELS - 1)

def addToBright(r1, r2):
    #print("length of darkList: ", len(darkList))
    if len(darkList) > 0:
        index = random.randint(r1, r2)
        while index >= len(darkList):
            index = random.randint(r1, r2)
        #print(index)
        brightList.append(darkList[index])
        colorsList[darkList[index]] = getRandomColor()
        darkList.pop(index)

def addToDark():
    item = brightList.pop()
    colorsList[item] = (0, 0, 0)
    darkList.append(item)

pixels.fill(BLACK)
pixels.show()
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples) / 10
    if magnitude > NUM_PIXELS - 1:
        magnitude = NUM_PIXELS - 1

    while len(brightList) < magnitude:
        addToBright(0, len(darkList))

    while len(brightList) > magnitude:
        addToDark()

    for x in brightList:
        pixels[x] = colorsList[x]
        pixels.show()
        
    for x in darkList:
        pixels[x] = BLACK
        pixels.show()

    print(((math.floor(magnitude)),))


    pixels.show()
    #time.sleep(0.005)