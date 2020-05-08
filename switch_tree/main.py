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
			motor_dir.value = not MOTOR_DIR_OUT
			led[0] = GREEN
		else:
			motor_dir.value = MOTOR_DIR_OUT
			led[0] = YELLOW
			cycle_number += 1
			if cycle_number == 3:
				time.sleep(2)
				pwm.duty_cycle = 0
				cycle_number = 0
				led[0] = BLUE
		time.sleep(0.5)






