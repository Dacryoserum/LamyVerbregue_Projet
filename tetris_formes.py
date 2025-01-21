import random
import pygame

# Couleurs pour les différentes formes
COLORS = [
    (0, 255, 255),  # Cyan (I)
    (0, 0, 255),    # Blue (J)
    (255, 165, 0),  # Orange (L)
    (255, 255, 0),  # Yellow (O)
    (0, 255, 0),    # Green (S)
    (128, 0, 128),  # Purple (T)
    (255, 0, 0),    # Red (Z)
]

# Définition des formes (les 4 rotations pour chaque forme)
SHAPES = {
    "I": [[(0, 1), (1, 1), (2, 1), (3, 1)]],
    "J": [[(0, 1), (1, 1), (2, 1), (2, 0)]],
    "L": [[(0, 1), (1, 1), (2, 1), (2, 2)]],
    "O": [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    "S": [[(1, 0), (2, 0), (0, 1), (1, 1)]],
    "T": [[(0, 1), (1, 1), (2, 1), (1, 0)]],
    "Z": [[(0, 0), (1, 0), (1, 1), (2, 1)]],
}

class Tetromino:
    def __init__(self, x, y, shape, grid_size):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.grid_size = grid_size
        self.rotation = 0

    def get_blocks(self):
        """Retourne les positions des blocs en fonction de la rotation actuelle."""
        return [(self.x + dx * self.grid_size, self.y + dy * self.grid_size)
                for dx, dy in SHAPES[self.shape][self.rotation]]

    def move_down(self):
        """Fait descendre la forme d'une unité."""
        self.y += self.grid_size

    def draw(self, screen):
        """Dessine la forme sur l'écran."""
        for block in self.get_blocks():
            pygame.draw.rect(screen, self.color, (*block, self.grid_size, self.grid_size))
