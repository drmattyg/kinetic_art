import time
import board
import pulseio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MOTOR_DIR_OUT = False
MOTOR_SPEED = int(65535/1.5)



led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
pwm = pulseio.PWMOut(board.A2, frequency=5000, duty_cycle=0)
motor_dir = DigitalInOut(board.D4)
motor_dir.direction = Direction.OUTPUT
motor_dir.value = MOTOR_DIR_OUT

limits = DigitalInOut(board.D3)
DEBOUNCE_NUM = 3
DEBOUNCE_SLEEP = 0.025
def get_switch(dev, debounce=DEBOUNCE_NUM):
	for i in range(DEBOUNCE_NUM):
		if not dev.value:
			return False
		time.sleep(DEBOUNCE_SLEEP)
	return True

def ramp_reverse(ramp_time=50, ramp_segments=10):
	# ramp_time is in ms
	pwm_val = MOTOR_SPEED
	initial_motor_dir = motor_dir.value
	delay_time = ramp_time/ramp_segments/1000
	delta = 2*MOTOR_SPEED/ramp_segments
	for i in range(ramp_segments):
		print(i)
		pwm_val = int(pwm_val - delta)
		if pwm_val < 0:
			motor_speed = -pwm_val
			motor_dir.value = (not initial_motor_dir)
		else:
			motor_speed = pwm_val
		pwm.duty_cycle = motor_speed
		time.sleep(delay_time)
	pwm.duty_cycle = MOTOR_SPEED


#limit_far = DigitalInOut(board.D2)
trigger = DigitalInOut(board.D1)
for pin in [limits, trigger]:
	pin.direction = Direction.INPUT
	pin.pull = Pull.DOWN

led[0] = BLUE
cycle_number = 0

while True:
	if get_switch(trigger):
		if cycle_number != 0:
			continue
		cycle_number = 1
		motor_dir.value = MOTOR_DIR_OUT
		pwm.duty_cycle = MOTOR_SPEED
		led[0] = YELLOW
		time.sleep(0.5)
	if get_switch(limits):
		if motor_dir.value == MOTOR_DIR_OUT:
			ramp_reverse()
			led[0] = GREEN
		else:
			ramp_reverse()
			led[0] = YELLOW
			cycle_number += 1
			if cycle_number == 3:
				time.sleep(2)
				pwm.duty_cycle = 0
				cycle_number = 0
				led[0] = BLUE
		time.sleep(0.5)






