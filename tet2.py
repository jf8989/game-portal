import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)  # Added this line

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED]

# Class for handling tetrominoes
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = -len(shape)  # Start slightly above the visible grid

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        pygame.Rect(
                            (self.x + col_idx) * BLOCK_SIZE,
                            (self.y + row_idx) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

# Check if position is valid
def valid_position(shape, grid, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if (
                    x + offset_x < 0
                    or x + offset_x >= GRID_WIDTH
                    or y + offset_y >= GRID_HEIGHT
                    or grid[y + offset_y][x + offset_x]
                ):
                    return False
    return True

# Add tetromino to grid and clear lines
def add_to_grid(shape, grid, offset_x, offset_y, color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + offset_y][x + offset_x] = color

    # Check for completed lines
    lines_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [BLACK] * GRID_WIDTH)
            lines_cleared += 1

    return lines_cleared

# Main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    score = 0

    current_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
    next_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))

    fall_time = 0
    game_over = False

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_over:
            print(f"Game Over! Your score: {score}")
            pygame.quit()
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and valid_position(current_tetromino.shape, grid, current_tetromino.x - 1, current_tetromino.y):
            current_tetromino.move(-1, 0)
        if keys[pygame.K_RIGHT] and valid_position(current_tetromino.shape, grid, current_tetromino.x + 1, current_tetromino.y):
            current_tetromino.move(1, 0)
        if keys[pygame.K_DOWN] and valid_position(current_tetromino.shape, grid, current_tetromino.x, current_tetromino.y + 1):
            current_tetromino.move(0, 1)
        if keys[pygame.K_UP]:
            rotated_shape = [list(row) for row in zip(*current_tetromino.shape[::-1])]
            if valid_position(rotated_shape, grid, current_tetromino.x, current_tetromino.y):
                current_tetromino.rotate()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > 500:  # Tetromino falls every 500ms
            fall_time = 0
            current_tetromino.move(0, 1)
            if not valid_position(current_tetromino.shape, grid, current_tetromino.x, current_tetromino.y):
                current_tetromino.move(0, -1)
                score += add_to_grid(current_tetromino.shape, grid, current_tetromino.x, current_tetromino.y, current_tetromino.color)
                current_tetromino = next_tetromino
                next_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
                # Check if the new tetromino has space to spawn
                if not valid_position(current_tetromino.shape, grid, current_tetromino.x, current_tetromino.y):
                    game_over = True

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != BLACK:
                    pygame.draw.rect(
                        screen,
                        cell,
                        pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

        current_tetromino.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()