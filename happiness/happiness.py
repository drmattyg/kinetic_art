from math import sqrt
import board
import displayio
from adafruit_ssd1351 import SSD1351
from analogio import AnalogIn
import time

def happiness(v, D=128):
    xv = []
    yv = []
    r = D/3 - 2*v*D/3 # D/3 -> -D/3
    x0 = D/2 - 6
    y0 = D/2 - v*(D/1.5 + 30) + 10
    for x in range(128):
        if abs(x - x0) <= abs(r):
            xv.append(x)
            y = -sqrt(r**2 - (x - x0)**2) + y0
            if v > 0.5:
                y = -y
            yv.append(int(y))
    return xv, yv

x1, y1 = happiness(0)
x2, y2 = happiness(1)
xc = len(x1)
yv = [0]*xc
def interp(s, k):
    return round(y2[k] + (y1[k] - y2[k])*s)

analog_in = AnalogIn(board.A1)

spi = board.SPI()
METRO_PINS = {
    'cs': board.D5,
    'dc': board.D6,
    'reset': board.D9
}

ITSY_BITSY_PINS =  {
    'cs': board.D7,
    'dc': board.D9,
    'reset': board.D10
}

PINS = ITSY_BITSY_PINS
tft_cs = PINS['cs']
tft_dc = PINS['dc']

displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=PINS['reset'])

display = SSD1351(display_bus, width=128, height=128)

bitmap = displayio.Bitmap(128, 128, 2)
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0x00ff00
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)
display.show(group)
while True:
    v = analog_in.value/65536
    c = len(x1)
    for i in range(xc):
        bitmap[yv[i], x1[i]] = 0
        yv[i] = interp(v, i)
        bitmap[yv[i], x1[i]] = 1

    time.sleep(0.01)
