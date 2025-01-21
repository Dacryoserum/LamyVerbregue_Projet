import pygame
from tetris_formes import Tetromino, SHAPES


pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30

GRAY = (0, 0, 0)
LIGHT_GRAY = (60, 60, 60)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

def draw_grid():
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y))
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GRAY)

        draw_grid()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
