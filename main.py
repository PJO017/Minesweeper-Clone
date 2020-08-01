import numpy as np
import pygame
import random as rd
from pygame import *

# Colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GRAY = (150, 150, 150)
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

MINES = 10

grid = np.array([[0 for x in range(0, GRID_SIZE)] for y in range(0, GRID_SIZE)])
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
font = pygame.font.Font('font/pixelfont.ttf', 15)

# Tile states and sprites
COVERED = 0
UNCOVERED = 1
FLAGGED = 2

MINE = 3
COV_MINE = 4
FLAG_MINE = 5

C = pygame.image.load('sprites/block.png').convert()
UC = pygame.image.load('sprites/empty.png').convert()
F = pygame.image.load('sprites/flagged.png').convert()
M = pygame.image.load('sprites/mine.png').convert()

block = pygame.transform.scale(C, (WIDTH, HEIGHT))
empty = pygame.transform.scale(UC, (WIDTH, HEIGHT))
flagged = pygame.transform.scale(F, (WIDTH, HEIGHT))
mine = pygame.transform.scale(M, (WIDTH, HEIGHT))

for i in range(0, MINES+1):
    grid[rd.randint(0, GRID_SIZE-1), rd.randint(0, GRID_SIZE-1)] = COV_MINE

# Check if a cell is valid
def isValid(row, col):
    if (row >= 0 and row <= GRID_SIZE-1) and (col >= 0 and col <= GRID_SIZE-1):
        return True
    else:
        return False

# check adjecent cells for mines
def check_adj_cells(row, col):

    #Check South
    if isValid(row+1, col):
        if grid[row+1, col] == COV_MINE:
            hint[row, col] += 1
    
    #Check North
    if isValid(row-1, col):
        if grid[row-1, col] == COV_MINE:
            hint[row, col] += 1

    #Check West
    if isValid(row, col-1):
        if grid[row, col-1] == COV_MINE:
            hint[row, col] += 1
    
    #Check East
    if isValid(row, col+1):
        if grid[row, col+1] == COV_MINE:
            hint[row, col] += 1

    #Check NorthWest
    if isValid(row-1, col-1):
        if grid[row-1, col-1] == COV_MINE:
            hint[row, col] += 1

    #Check NorthEast
    if isValid(row-1, col+1):
        if grid[row-1, col+1] == COV_MINE:
            hint[row, col] += 1

    #Check SouthEast
    if isValid(row+1, col+1):
        if grid[row+1, col+1] == COV_MINE:
            hint[row, col] += 1

    #Check SouthWest
    if isValid(row+1, col-1):
        if grid[row+1, col-1] == COV_MINE:
            hint[row, col] += 1

# Clear adjecent cells
def clear_adj_cells(row, col):
   #Check South
    if isValid(row+1, col):
        if grid[row+1, col] != COV_MINE:
            grid[row+1, col] = UNCOVERED
            
    
    #Check North
    if isValid(row-1, col):
        if grid[row-1, col] != COV_MINE:
            grid[row-1, col] = UNCOVERED
            
    #Check West
    if isValid(row, col-1):
        if grid[row, col-1] != COV_MINE:
            grid[row, col-1] = UNCOVERED
           
    
    #Check East
    if isValid(row, col+1):
        if grid[row, col+1] != COV_MINE:
            grid[row, col+1] = UNCOVERED
         


    #Check NorthWest
    if isValid(row-1, col-1):
        if grid[row-1, col-1] != COV_MINE:
            grid[row-1, col-1] = UNCOVERED
        

    #Check NorthEast
    if isValid(row-1, col+1):
        if grid[row-1, col+1] != COV_MINE:
            grid[row-1, col+1] = UNCOVERED
           

    #Check SouthEast
    if isValid(row+1, col+1):
        if grid[row+1, col+1] != COV_MINE:
            grid[row+1, col+1] = UNCOVERED
           

    #Check SouthWest
    if isValid(row+1, col-1):
        if grid[row+1, col-1] != COV_MINE:
            grid[row+1, col-1] = UNCOVERED
             

# Create Hints
for row in range(0, GRID_SIZE):
    for col in range(0, GRID_SIZE):
        check_adj_cells(row, col)


# Draw grid
def draw_grid():
    for row in range(0, GRID_SIZE):
        for col in range(0, GRID_SIZE):

            if grid[row, col] == COVERED or grid[row, col] == COV_MINE: 
                screen.blit(block, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN))

            if grid[row, col] == UNCOVERED:   
                screen.blit(empty, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN))

                num = hint[row, col]
                if num == 0:
                    clear_adj_cells(row, col)
                else:
                    cell_hint = font.render(str(num), True, BLUE)
                    screen.blit(cell_hint, ((WIDTH + MARGIN) * col + MARGIN + 5, (HEIGHT + MARGIN) * row + MARGIN))

            if grid[row, col] == FLAGGED or grid[row, col] == FLAG_MINE:
                screen.blit(flagged, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN))

            if grid[row, col] == MINE:
                screen.blit(mine, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN))


def show_game():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col] == COV_MINE:
                grid[row, col] = MINE

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

            # CLick covered block
            if grid[row, col] == COVERED:
                if event.button == 1:
                    grid[row, col] = UNCOVERED
                elif event.button == 3:
                    grid[row, col] = FLAGGED

            # Click covered mine
            elif grid[row, col] == COV_MINE:
                if event.button == 1:
                    grid[row, col] = MINE
                    show_game()
                    print('YOU LOSE')
                elif event.button == 3:
                    grid[row, col] = FLAG_MINE

            # Click flagged block
            elif grid[row, col] == FLAGGED:
                if event.button == 3:
                    grid[row, col] = COVERED

            # CLick flagged mine
            elif grid[row, col] == FLAG_MINE:
                if event.button == 3:
                    grid[row, col] = COV_MINE

        


    # Set background to black
    screen.fill(BLACK)
        

    # Draw grid
    draw_grid()        

    # Show Screen
    pygame.display.flip()

pygame.quit()
