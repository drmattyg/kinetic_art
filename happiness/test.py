import pygame

WHITE = (255, 255, 255)
SIZE = (128, 128)
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    surf = pygame.Surface(SIZE)
    surf.fill(WHITE)

    screen.blit(surf, (0, 0))

    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
    pygame.quit()


if __name__ == '__main__':
    main()