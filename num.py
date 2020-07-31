import numpy as np
import pygame
from pygame import *

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Width and Height of each cell
WIDTH = 20
HEIGHT = 20

# Margin b/w each cell
MARGIN = 2

# Grid size row x col
GRID_SIZE = 10

grid = np.array([[0 for x in range(0, GRID_SIZE)] for y in range(0, GRID_SIZE)])

# Initialize pygame
pygame.init()

# Create display
SCRN_W = ((GRID_SIZE + 1) * MARGIN) + (GRID_SIZE * WIDTH)
SCRN_H = ((GRID_SIZE + 1) * MARGIN) + (GRID_SIZE * WIDTH)

screen = pygame.display.set_mode((SCRN_W, SCRN_H))
icon = pygame.image.load('icon.png')
icon = pygame.Surface(icon.get_rect())
pygame.display.set_icon(icon)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for click
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            pos = pygame.mouse.get_pos()
            col = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            grid[row, col] = 1

    # Set background to black
    screen.fill((0, 0, 0))

    # Draw grid
    for row in range(0, GRID_SIZE):
        for col in range(0, GRID_SIZE):
            color = (255, 255, 255)
            if grid[row, col] == 1:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))

    

    
    pygame.display.flip()

pygame.quit()
