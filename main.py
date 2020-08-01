import numpy as np
import pygame
import random as rd
from pygame import *

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (160, 160, 160)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --------- GRID --------------------
# Width and Height of each cell
WIDTH = 20
HEIGHT = 20

# Margin b/w each cell
MARGIN = 2

# Grid size row x col
GRID_SIZE = 10

grid = np.array([[1 for x in range(0, GRID_SIZE)] for y in range(0, GRID_SIZE)])
hint = np.array([[0 for x in range(0, GRID_SIZE)] for y in range(0, GRID_SIZE)])

# ---------- LOGIC ---------------------
# Initialize pygame
pygame.init()

# Create display
SCRN_W = ((GRID_SIZE + 1) * MARGIN) + (GRID_SIZE * WIDTH)
SCRN_H = ((GRID_SIZE + 1) * MARGIN) + (GRID_SIZE * WIDTH)

screen = pygame.display.set_mode((SCRN_W, SCRN_H))
pygame.display.set_caption('Minesweeper')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Font Stuff 
font = pygame.font.Font('pixelfont.ttf', 15)

text = font.render('1', True, BLACK)


# Tile states
COVERED = 0
UNCOVERED = 1
FLAGGED = 2
MINE = 3

for i in range(0, 10):
    grid[rd.randint(0, 9), rd.randint(0, 9)] = MINE

def isValid(row, col):
    if (row >= 0 and row <= GRID_SIZE-1) and (col >= 0 and col <= GRID_SIZE-1):
        return True
    else:
        return False

def check_adj_cells(row, col):

    #Check South
    if isValid(row+1, col):
        if grid[row+1, col] == MINE:
            hint[row, col] += 1
    
    #Check North
    if isValid(row-1, col):
        if grid[row-1, col] == MINE:
            hint[row, col] += 1

    #Check West
    if isValid(row, col-1):
        if grid[row, col-1] == MINE:
            hint[row, col] += 1
    
    #Check East
    if isValid(row, col+1):
        if grid[row, col+1] == MINE:
            hint[row, col] += 1

    #Check NorthWest
    if isValid(row-1, col-1):
        if grid[row-1, col-1] == MINE:
            hint[row, col] += 1

    #Check NorthEast
    if isValid(row-1, col+1):
        if grid[row-1, col+1] == MINE:
            hint[row, col] += 1

    #Check SouthEast
    if isValid(row+1, col+1):
        if grid[row+1, col+1] == MINE:
            hint[row, col] += 1

    #Check SouthWest
    if isValid(row+1, col-1):
        if grid[row+1, col-1] == MINE:
            hint[row, col] += 1

# Create Hints
for row in range(0, GRID_SIZE-1):
    for col in range(0, GRID_SIZE-1):
        check_adj_cells(row, col)


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

            if grid[row, col] == COVERED:
                if event.button == 1:
                    grid[row, col] = UNCOVERED

                elif event.button == 3:
                    grid[row, col] = FLAGGED

            elif grid[row, col] == FLAGGED:
                if event.button == 3:
                    grid[row, col] = COVERED


    # Set background to black
    screen.fill(BLACK)

    # Draw grid
    for row in range(0, GRID_SIZE):
        for col in range(0, GRID_SIZE):
            color = (GRAY)
            if grid[row, col] == UNCOVERED:
                color = WHITE
            elif grid[row, col] == FLAGGED:
                color = BLUE
            elif grid[row, col] == MINE:
                color = RED
            cell = pygame.Rect(((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            pygame.draw.rect(screen, color, cell)

            if grid[row, col] == UNCOVERED:
                if hint[row, col] != 0:
                    cell_hint = font.render(str(hint[row, col]), True, BLACK)
                    screen.blit(cell_hint, ((WIDTH + MARGIN) * col + MARGIN + 5, (HEIGHT + MARGIN) * row + MARGIN))
            

            

    # Show Screen
    pygame.display.flip()

pygame.quit()
