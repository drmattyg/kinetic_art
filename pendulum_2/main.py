import board
from time import sleep
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import adafruit_vl53l0x
import busio
from adafruit_motor import servo
import pwmio

DELAY = 40
THRESHOLD = 50000
POLL_TIME = 1

# initialize
def init_audio_output(d):
    out = DigitalInOut(d)
    out.direction = Direction.OUTPUT
    out.value = False
    return out

# audio relays
[audio1, audio2] = [init_audio_output(d) for d in [board.D3, board.D4]]

# rail sensors
[sense1, sense2] = [AnalogIn(d) for d in [board.A1, board.A2]]

# LEFT OFF HERE FIX SERVO CODE
pwms = [pwmio.PWMOut(_pin, duty_cycle=2 ** 15, frequency=50) for _pin in [board.A6, board.A7]
[servo1, servo2] = [servo.Servo(_pwm) for _pwm in pwms]

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

def tilt_servo(s, degrees=15, pause_time=0.5, lr=True, servo_cycle_wait=0.02):
    # Assume servo starts at center (90 degrees)
    center_position = 90

    # Tilt direction: left if lr is True, right if lr is False
    if lr:
        target_position = center_position - degrees  # Tilt to the left by n degrees
    else:
        target_position = center_position + degrees  # Tilt to the right by n degrees

    # Smoothly tilt to the target position
    step = -1 if lr else 1
    for angle in range(center_position, target_position + step, step):
        s.angle = angle
        time.sleep(servo_cycle_wait)  # Adjust this value for smoother or faster movement

    # Pause for t seconds
    time.sleep(pause_time)

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

    # to tilt or not to tilt?
    # every POLL_TIME seconds, pick a random number, and if it is lower than the threshold, tilt.
    # if ON, which is (auto_mode | distance < distance_threshold)


