import sys
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

if __name__ == '__main__':
    main()
