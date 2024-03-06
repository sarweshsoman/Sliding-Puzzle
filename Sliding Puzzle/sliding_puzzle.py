import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up constants
GRID_SIZE = 4
TILE_SIZE = 100
PANEL_WIDTH = 400  # Increased width for the reference image panel
PANEL_HEIGHT = GRID_SIZE * TILE_SIZE
PARTITION_WIDTH = 5  # Width of the partition line

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and prepare the image
image = pygame.image.load("starry_night.jpeg")  # Replace with the path to your image
image = pygame.transform.scale(image, (GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE))

# Cut the image into pieces for each tile
tile_size = TILE_SIZE
image_pieces = [[image.subsurface(j * tile_size, i * tile_size, tile_size, tile_size) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

# Helper function to draw the puzzle board
def draw_board(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

# Helper function to shuffle the puzzle tiles
def shuffle_board(board):
    flat_board = [tile for row in board for tile in row]
    random.shuffle(flat_board)
    shuffled_board = [flat_board[i:i + GRID_SIZE] for i in range(0, len(flat_board), GRID_SIZE)]
    return shuffled_board

# Set up the game window
WIDTH = GRID_SIZE * TILE_SIZE + PANEL_WIDTH + PARTITION_WIDTH
HEIGHT = max(GRID_SIZE * TILE_SIZE, PANEL_HEIGHT)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")

# Create the initial game board with image pieces
puzzle_board = [[image_pieces[i][j] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
puzzle_board[GRID_SIZE - 1][GRID_SIZE - 1] = None  # Empty tile

# Shuffle the puzzle board
puzzle_board = shuffle_board(puzzle_board)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Check arrow key input to move tiles
            empty_row, empty_col = next((i, j) for i, row in enumerate(puzzle_board) for j, tile in enumerate(row) if tile is None)

            if event.key == pygame.K_UP and empty_row < GRID_SIZE - 1:
                puzzle_board[empty_row][empty_col], puzzle_board[empty_row + 1][empty_col] = puzzle_board[empty_row + 1][empty_col], puzzle_board[empty_row][empty_col]
            elif event.key == pygame.K_DOWN and empty_row > 0:
                puzzle_board[empty_row][empty_col], puzzle_board[empty_row - 1][empty_col] = puzzle_board[empty_row - 1][empty_col], puzzle_board[empty_row][empty_col]
            elif event.key == pygame.K_LEFT and empty_col < GRID_SIZE - 1:
                puzzle_board[empty_row][empty_col], puzzle_board[empty_row][empty_col + 1] = puzzle_board[empty_row][empty_col + 1], puzzle_board[empty_row][empty_col]
            elif event.key == pygame.K_RIGHT and empty_col > 0:
                puzzle_board[empty_row][empty_col], puzzle_board[empty_row][empty_col - 1] = puzzle_board[empty_row][empty_col - 1], puzzle_board[empty_row][empty_col]

    # Clear the screen
    screen.fill(BLACK)

    # Draw the puzzle board
    draw_board(puzzle_board)

    # Draw the partition line
    pygame.draw.line(screen, WHITE, (GRID_SIZE * TILE_SIZE, 0), (GRID_SIZE * TILE_SIZE, HEIGHT), PARTITION_WIDTH)

    # Draw the reference image panel
    pygame.draw.rect(screen, WHITE, (GRID_SIZE * TILE_SIZE + PARTITION_WIDTH, 0, PANEL_WIDTH, PANEL_HEIGHT))
    screen.blit(image, (GRID_SIZE * TILE_SIZE + PARTITION_WIDTH, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
