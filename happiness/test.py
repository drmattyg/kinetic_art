from time import sleep

import pygame
import numpy as np
from math import sqrt
BLACK = (0, 0, 0)
SIZE = (128, 128)
def hv(v, D=128):
    xv = []
    yv = []
    r = D/3 - 2*v*D/3 # D/3 -> -D/3
    x0 = D/2
    y0 = D/2 - D*v/1.5
    for x in range(128):
        if abs(x - x0) <= abs(r):
            xv.append(x)
            y = -sqrt(r**2 - (x - x0)**2) + y0
            if v > 0.5:
                y = -y
            yv.append(y)
    return xv, yv

x1, y1 = hv(0)
x2, y2 = hv(1)
def interp(s, k):
    return round(y2[k] + (y1[k] - y2[k])*s)

GREEN = pygame.Color(0, 255, 0)
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    surf = pygame.Surface(SIZE)
    v = 0
    dvabs = 0.01
    dv = dvabs
    pygame.time.set_timer(10, 50)
    while True:
        v += dv
        if v <= 0:
            v = 0
            dv = dvabs
        if v >= 1:
            v = 1
            dv = -dvabs

        # test

        surf.fill(0)
        pxarr = pygame.PixelArray(surf)
        for i in range(len(x1)):
            x = x1[i]
            y = interp(v, i)
            pxarr[x, y] = GREEN
        pxarr.close()
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
    pygame.quit()





if __name__ == '__main__':
    main()