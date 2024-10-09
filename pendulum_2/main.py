import board
from time import sleep, monotonic
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import adafruit_vl53l0x
import busio
from adafruit_motor import servo
import pwmio
from random import random, choice

DELAY = 40
THRESHOLD = 50000
POLL_TIME = 1000 # ms
TILT_THRESHOLD = 0.2
SERVO_STEP = 0.2
SERVO_TARGETS = [5, 5]
SERVO_CENTERS = [90, 90]
POLL_TIME = 1
TEST = True

# initialize
def init_audio_output(d):
    out = DigitalInOut(d)
    out.direction = Direction.OUTPUT
    out.value = False
    return out

# audio relays
audios = [init_audio_output(d) for d in [board.D3, board.D4]]

# rail sensors
sensors = [AnalogIn(d) for d in [board.A1, board.A2]]

def init_servo(pin):
    return servo.Servo(pwmio.PWMOut(pin, duty_cycle=2 ** 15, frequency=50))
servos = [init_servo(pin) for pin in [board.A13, board.A14]

# distance sensor
# i2c = busio.I2C(board.SCL, board.SDA)
# tof = adafruit_vl53l0x.VL53L0X(i2c)
# tof.range is the range in mm

# mode switch
mode = DigitalInOut(board.D13)
mode.direction = Direction.INPUT
mode.pull = digitalio.Pull.UP
def is_ranging_mode():
    return mode.value

# rail sensor threshold counter
sensor_threshold_counters = [0, 0]

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


t0 = monotonic()
t_poll = t0
t_servo = t0
servo_targets = list(SERVO_CENTERS)
servo_lr = [1, 1]
while True:
    if TEST:
        print("sense1: ", sense1.value)
        print("sense2: ", sense2.value)
        print("mode: ", mode.value)
    else:
        # switch the audio output based on sensor mode
        sense_n1, b1 = debounce(sense_n1, sense1)
        sense_n2, b2 = debounce(sense_n2, sense2)
        audio1.value = b1
        audio2.value = b2


    # to tilt or not to tilt?
    # every POLL_TIME ms, pick a random number, and if it is lower than the threshold, tilt.
    # if ON, which is (auto_mode | distance < distance_threshold)
    if (monotonic() - t0) > POLL_TIME:
        t0 = monotonic()
        if random() < TILT_THRESHOLD:
            # pick top or bottom
            tb = choice([0, 1])
            if servo_targets[tb] != servos[tb].angle:
            # pick lr and set the servo target
            servo_lr[tb] = choice([1, -1])
            servo_targets[tb] = SERVO_CENTERS[tb] + lr*SERVO_TARGETS[tb]

    for i in [0, 1]:
        if servo_target[tb] != servos[tb].angle:
            servos[tb].angle = servos[tb].angle + servo_lr[tb]*SERVO_STEP
