import time
import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction
i2c = board.I2C()
mcp = MCP23017(i2c, address=0x20)
while not i2c.try_lock():
    pass

try:
    while True:
        print("I2C addresses found:", [hex(device_address)
              for device_address in i2c.scan()])
        time.sleep(2)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()

