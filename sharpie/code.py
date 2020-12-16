import time
import adafruit_dotstar
import board
from digitalio import Direction, DigitalInOut, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
import busio
import touchio

touch_pad = board.A4
touch = touchio.TouchIn(touch_pad)
I2C_ADDR = 0x20

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

COLORS = [GREEN, BLUE, YELLOW, RED]




led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led[0] = RED

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=I2C_ADDR)
KEYS = {'2': 0, '0': 1, 'P': 2, 'C': 3}

def keypress(k, duration = 0.25):
	p = mcp.get_pin(KEYS[str(k)])
	p.value = True
	time.sleep(duration)
	p.value = False


for n in range(16):
	pin = mcp.get_pin(n)
	pin.direction = Direction.OUTPUT
	pin.value = False


led[0]= RED
n = 0
while(True):
	if touch.value:
		print(n)
		mcp.get_pin(n).value = True
		mcp.get_pin((n - 1)%16).value = False
		led[0] = COLORS[n % 4]
		time.sleep(0.5)
		n+= 1


