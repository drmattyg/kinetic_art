import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep, monotonic
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
servos = [init_servo(pin) for pin in [board.A13, board.A14]]

# distance sensor
# i2c = busio.I2C(board.SCL, board.SDA)
# tof = adafruit_vl53l0x.VL53L0X(i2c)
# tof.range is the range in mm

# mode switch
mode = DigitalInOut(board.D13)
mode.direction = Direction.INPUT
mode.pull = Pull.UP
def is_ranging_mode():
    return mode.value

sensor_threshold = [0, 0]
# rail sensor threshold counter
sensor_threshold_counters = [0, 0]
sensor_delay = [DELAY, DELAY]

t0 = monotonic()

# def tilt_servo(s, degrees=15, pause_time=0.5, lr=True, servo_cycle_wait=0.02):
#     # Assume servo starts at center (90 degrees)
#     center_position = 90

#     # Tilt direction: left if lr is True, right if lr is False
#     if lr:
#         target_position = center_position - degrees  # Tilt to the left by n degrees
#     else:
#         target_position = center_position + degrees  # Tilt to the right by n degrees

#     # Smoothly tilt to the target position
#     step = -1 if lr else 1
#     for angle in range(center_position, target_position + step, step):
#         s.angle = angle
#         time.sleep(servo_cycle_wait)  # Adjust this value for smoother or faster movement

#     # Pause for t seconds
#     time.sleep(pause_time)

def debounce(i):
    n = sensor_threshold_counters[i]
    v = sensors[i].value
    if v < sensor_threshold[i]:
        n = 1
    else:
        if n == 0:
            return 0, False
        n += 1
        if n > sensor_delay[i]:
            n = 0
    if n == 0:
        b = False
    else:
        b = True
    return n, b



t_poll = t0
t_servo = t0
servo_targets = list(SERVO_CENTERS)
servo_lr = [1, 1] # set the sense (positive or negative) of the servo target direction
servo_moving = [0, 0] # 0 = Not moving, 1 = Moving out, 2 = Moving back
while True:
    # if TEST:
    #     print("sense1: ", sense1.value)
    #     print("sense2: ", sense2.value)
    #     print("mode: ", mode.value)
    #     print("range:", tof.range)
    # else:
        # switch the audio output based on sensor mode
    for i in [0, 1]:
        sensor_threshold_counters[i], b = debounce(i)
        audios[i].value = b


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

            # set the servo target angle
            servo_targets[tb] = SERVO_CENTERS[tb] + lr*SERVO_TARGETS[tb]
            servo_moving[tb] = 1

    # rock the servo out and back
    for i in [0, 1]:
        if servo_target[tb] != servos[tb].angle: # if we're not at our target angle
            servos[tb].angle = servos[tb].angle + servo_lr[tb]*SERVO_STEP #take a step towards our target angle
        else:
            if servo_moving[tb] == 1:  # if we're at the target, and we're still in motion
                servo_target[tb] = SERVO_CENTERS[tb] # set the target back to the center
                servo_lr[tb] = -servo_lr[tb] # reverse direction
            elif servo_moving[tb] == 2: # if we were on our way back and we're at the target angle
                servo_moving[tb] = 0 # stop moving

