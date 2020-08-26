import pygame
import numpy as np
BLACK = (0, 0, 0)
SIZE = (128, 128)
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    surf = pygame.surfarray.make_surface()



    screen.blit(surf, (0, 0))

    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
    pygame.quit()

def generate_graticule(count=3):
    d = int(SIZE[0]*2/count)
    a = np.zeros(SIZE)
    x0 = SIZE[0]/2
    y0 = SIZE[1]/2
    for i in range(count):
        a[x0 + d*i, :] = 1
        a[x0 - d*i, :] = 1
        a[:, y0 + d*i] = 1
        a[:, y0 - d*i] = 1

    return a

def np_to_dict(n):
    a = n.tolist()
    d = {}
    for i, row in enumerate(a):
        for j, col in enumerate(row):
            if col > 0:
                d[(i, j)] = col
    return d





if __name__ == '__main__':
    main()