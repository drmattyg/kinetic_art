import board
from time import sleep
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn

DELAY = 40
THRESHOLD = 50000

out1 = DigitalInOut(board.D3)
out1.direction = Direction.OUTPUT
out2 = DigitalInOut(board.D4)
out2.direction = Direction.OUTPUT
out1.value = False
out2.value = False
in1 = AnalogIn(board.A1)
in2 = AnalogIn(board.A2)
n1 = 0
n2 = 0

def switch(n, v):
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
    n1, b1 = switch(n1, in1.value)
    n2, b2 = switch(n2, in2.value)
    out1.value = b1
    out2.value = b2
