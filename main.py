import numpy as np
import pygame
import random as rd
import os
from pygame import *

# Colors
BLACK = Color(0, 0, 0)
WHITE = Color(200, 200, 200)
GRAY = Color(150, 150, 150)
RED = Color(255, 100, 0, 50)
BLUE = Color(0, 0, 255, 50)
      
# ---------- LOGIC ---------------------
# Initialize pygame
pygame.init()

# --------- GRID --------------------
# Width and Height of each cell
WIDTH = 30
HEIGHT = 30

# Margin b/w each cell
MARGIN = 0

# Grid size row x col
GRID_SIZE = 10

MINES = 10

# Create display
SCRN_W = ((GRID_SIZE + 1) * MARGIN) + (GRID_SIZE * WIDTH)
SCRN_H = ((GRID_SIZE + 1) * MARGIN) + (GRID_SIZE * WIDTH)

screen = pygame.display.set_mode((SCRN_W, SCRN_H))
pygame.display.set_caption('Minesweeper')

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Font Stuff 
font = pygame.font.Font('font/pixelfont.ttf', 15)


# Loading sprites
C = pygame.image.load('sprites/block.png').convert()
UC = pygame.image.load('sprites/empty.png').convert()
F = pygame.image.load('sprites/flagged.png').convert()
M = pygame.image.load('sprites/mine.png').convert()
RM = pygame.image.load('sprites/red_mine.png').convert()
CM = pygame.image.load('sprites/crossed_mine.png')

# Scaling sprites
block = pygame.transform.scale(C, (WIDTH, HEIGHT))
empty = pygame.transform.scale(UC, (WIDTH, HEIGHT))
flagged = pygame.transform.scale(F, (WIDTH, HEIGHT))
mine = pygame.transform.scale(M, (WIDTH, HEIGHT))
red_mine = pygame.transform.scale(RM, (WIDTH, HEIGHT))
cross_mine = pygame.transform.scale(CM, (WIDTH, HEIGHT))

# Load the number sprites
def load_numbers(path_to_directory):
    """Load all images from subdirectories and return them as a dict."""
    images = {}

    for dirpath, dirnames, filenames in os.walk(path_to_directory):
        for name in filenames:
            if name.endswith('.png'):
                key = name[0]
                img = pygame.image.load(os.path.join(dirpath, name)).convert()
                new_img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                images[key] = new_img    
    return images

numbers = load_numbers('sprites/numbers')

class Tile():
    def __init__(self):
        self.mine = False
        self.covered = True
        self.flagged = False
        self.hint = 0
        self.image = block

        
    def clicked(self, click, row=None, col=None):

        if click == 1:
            if self.covered and not self.mine and not self.flagged:
                self.covered = False 
                if self.hint > 0:
                    self.image = numbers[str(self.hint)]
                else:
                    clear_adj_cells(row, col)
                    self.image = empty


            if self.covered and self.mine and not self.flagged:
                loss()
                self.image = red_mine            

        if click == 3:
            if self.covered and not self.flagged:
                self.flagged = True
                self.image = flagged

            elif self.flagged:
                self.flagged = False
                self.image = block
        
grid = np.array([[Tile() for x in range(0, GRID_SIZE)] for y in range(0, GRID_SIZE)])


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
        if grid[row+1, col].mine and grid[row+1, col].covered:
            grid[row, col].hint += 1
    
    #Check North
    if isValid(row-1, col):
        if grid[row-1, col].mine and grid[row-1, col].covered:
            grid[row, col].hint += 1

    #Check West
    if isValid(row, col-1):
        if grid[row, col-1].mine and grid[row, col-1].covered:
            grid[row, col].hint += 1
    
    #Check East
    if isValid(row, col+1):
        if grid[row, col+1].mine and grid[row, col+1].covered:
            grid[row, col].hint += 1

    #Check NorthWest
    if isValid(row-1, col-1):
        if grid[row-1, col-1].mine and grid[row-1, col-1].covered:
            grid[row, col].hint += 1

    #Check NorthEast
    if isValid(row-1, col+1):
        if grid[row-1, col+1].mine and grid[row-1, col+1].covered:
            grid[row, col].hint += 1

    #Check SouthEast
    if isValid(row+1, col+1):
        if grid[row+1, col+1].mine and grid[row+1, col+1].covered:
            grid[row, col].hint += 1

    #Check SouthWest
    if isValid(row+1, col-1):
        if grid[row+1, col-1].mine and grid[row+1, col-1].covered:
            grid[row, col].hint += 1

def clear_adj_cells(row, col):
    #Check South
    if isValid(row+1, col):
       grid[row+1, col].clicked(1, row+1, col)
    
    #Check North
    if isValid(row-1, col):
        grid[row-1, col].clicked(1, row-1, col)

    #Check West
    if isValid(row, col-1):
        grid[row, col-1].clicked(1, row, col-1)
    
    #Check East
    if isValid(row, col+1):
        grid[row, col+1].clicked(1, row, col+1)

    #Check NorthWest
    if isValid(row-1, col-1):
        grid[row-1, col-1].clicked(1, row-1, col-1)

    #Check NorthEast
    if isValid(row-1, col+1):
        grid[row-1, col+1].clicked(1, row-1, col+1)

    #Check SouthEast
    if isValid(row+1, col+1):
        grid[row+1, col+1].clicked(1, row+1, col+1)

    #Check SouthWest
    if isValid(row+1, col-1):
        grid[row+1, col-1].clicked(1, row+1, col-1)

# Draw grid
def draw_grid(): 
    for row in range(0, GRID_SIZE):
        for col in range(0, GRID_SIZE):
            screen.blit(grid[row, col].image, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN))
            
def create_game():
    for i in range(0, 11):
        x = rd.randint(0, GRID_SIZE-1)
        y = rd.randint(0, GRID_SIZE-1)

        grid[x, y].mine = True
        # grid[x, y].image = mine

    for row in range(0, GRID_SIZE):
        for col in range(0, GRID_SIZE):
            check_adj_cells(row, col) 

win = False
lost = False

def check_win():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col].covered and not grid[row, col].mine:
                return False
    return True     

def won():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col].mine and not grid[row, col].flagged:
                grid[row, col].flagged = True
                grid[row, col].image = flagged

    pygame.draw.rect(screen, BLUE, Rect(100, 100, 105, 50))
    win_text = font.render("YOU WIN", True, WHITE)
    screen.blit(win_text, (110, 110))

def loss():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col].mine and grid[row, col].covered:
                grid[row, col].mine = True
                grid[row, col].image = mine
            if grid[row, col].covered and not grid[row, col].mine and grid[row, col].flagged:
                grid[row, col].image = cross_mine
                grid[row, col].mine = True

    pygame.draw.rect(screen, RED, Rect(100, 100, 105, 50))
    lose_text = font.render("YOU LOSE", True, WHITE)
    screen.blit(lose_text, (110, 110))


create_game()

# Main loop
def game():
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

                if event.button == 1:
                    grid[row, col].clicked(1, row, col)
                elif event.button == 3:
                    grid[row, col].clicked(3)


        # Set background to black
        screen.fill(BLACK)
            
        # Draw grid
        draw_grid() 

        if check_win():
            won()

        pygame.display.flip()


game()
pygame.quit()
    
