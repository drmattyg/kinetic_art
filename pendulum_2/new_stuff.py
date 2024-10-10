import board
from analogio import AnalogIn
from digitalio import Direction, DigitalInOut
import time
#import pwmio
#from adafruit_motor import servo

toprail = AnalogIn(board.A0)
btmrail = AnalogIn(board.A1)

relay1 = DigitalInOut(board.D5)
relay1.direction = Direction.OUTPUT

relay2 = DigitalInOut(board.D7)
relay2.direction = Direction.OUTPUT

#pwm1 = pwmio.PWMOut(board.A5, duty_cycle=2 ** 15, frequency=50)

#servo1 = servo.Servo(pwm1)
#servo1.angle = 90

while True:
    print((toprail.value, btmrail.value))
    relay1.value = True
    relay2.value = True
    time.sleep(0.5)
    relay1.value = False
    relay2.value = False
    time.sleep(0.5)# Write your code here :-)
