import board
import pulseio
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
MAXV = 65535
MIN_SPEED = 7
out_pins = [board.D10, board.D11, board.D12, board.D13]
outs = [pulseio.PWMOut(p, frequency=5000, duty_cycle=0) for p in out_pins]
def pwmv(v):
	return int(v*MAXV/100)

def set_speed(pin, v):
	# v = 0 to 100
	outs[i].duty_cycle = pwmv(v)

def set_all(v):
	for out in outs:
		out.duty_cycle = pwmv(v)

def ramp_all(v, steps=10, delay=1):
	step_size = [(pwmv(v) - out.duty_cycle)/steps for out in outs]
	for i in range(steps):
		for n, out in enumerate(outs):
			out.duty_cycle = int(step_size[n]*(i + 1))
set_all(0)
sleep(1)
ramp_all(50)
sleep(0.25)
for i, v in enumerate([7, 9, 13, 20]):
	set_speed(i, v)
while True:
	pass
