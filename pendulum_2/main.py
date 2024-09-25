import board
from time import sleep
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import adafruit_vl53l0x
import busio

DELAY = 40
THRESHOLD = 50000

# initialize
def init_audio_output(d):
    out = DigitalInOut(d)
    out.direction = Direction.OUTPUT
    out.value = False
    return out

# audio relays
audio1 = init_audio_output(board.D3)
audio2 = init_audio_output(board.D4)

# rail sensors
sense1 = AnalogIn(board.A1)
sense2 = AnalogIn(board.A2)

# distance sensor
i2c = busio.I2C(board.SCL, board.SDA)
tof = adafruit_vl53l0x.VL53L0X(i2c)
# tof.range is the range in mm

# mode switch
mode = DigitalInOut(board.D5)
mode.direction = Direction.INPUT
mode.pull = digitalio.Pull.UP
def is_ranging_mode():
    return mode.value

# rail sensor threshold counter
sense_n1 = 0
sense_n2 = 0

def debounce(n, v):

    if v < THRESHOLD:
        n = 1
    else:
        if n == 0:
            return 0, False
        n += 1
        if n > DELAY:
            n = 0
    if n == 0:
        b = False
    else:
        b = True
    return n, b

while True:
    # switch the audio output based on sensor mode
    sense_n1, b1 = debounce(sense_n1, sense1)
    sense_n2, b2 = debounce(sense_n2, sense2)
    audio1.value = b1
    audio2.value = b2


