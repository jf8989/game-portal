import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [['.....',
      '.....',
      '.....',
      'XXXX.',
      '.....'],
     ['..X..',
      '..X..',
      '..X..',
      '..X..',
      '.....']],

    [['.....',
      '.....',
      '..XX.',
      '..XX.',
      '.....']],

    [['.....',
      '.....',
      '..XXX',
      '...X.',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '..X..',
      '.....'],
     ['.....',
      '...X.',
      '..XXX',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '..X..',
      '.....']],

    [['.....',
      '.....',
      '..XXX',
      '..X..',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '..X..',
      '.....'],
     ['.....',
      '..X..',
      '..XXX',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '..X..',
      '.....']],

    [['.....',
      '.....',
      '..XXX',
      'X....',
      '.....'],
     ['.....',
      'XX...',
      '.X...',
      '.X...',
      '.....'],
     ['.....',
      '...X.',
      'XXX..',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '..XX.',
      '.....']],

    [['.....',
      '.....',
      '..XX.',
      '...XX',
      '.....'],
     ['.....',
      '...X.',
      '..XX.',
      '..X..',
      '.....']],

    [['.....',
      '.....',
      'XX...',
      '.XX..',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '.X...',
      '.....']]
]

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_shape(self):
        return self.shape[self.rotation]

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (j, i) in locked_positions:
                color = locked_positions[(j, i)]
                grid[i][j] = color
    return grid

def convert_shape_format(tetromino):
    positions = []
    shape_format = tetromino.get_shape()

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                positions.append((tetromino.x + j, tetromino.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(tetromino, grid):
    accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(tetromino)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def draw_grid(screen, grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for i in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, WHITE, (0, i * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, i * BLOCK_SIZE))
    for j in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, WHITE, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))

def draw_tetromino(screen, tetromino):
    shape_format = convert_shape_format(tetromino)
    for pos in shape_format:
        if pos[1] > -1:
            pygame.draw.rect(screen, tetromino.color,
                             (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def clear_rows(grid, locked):
    inc = 0
    for i in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < inc:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    current_piece = Tetromino(5, 0)
    next_piece = Tetromino(5, 0)

    font = pygame.font.SysFont('comicsans', 30, True)

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        shape_pos = convert_shape_format(current_piece)

        for i, pos in enumerate(shape_pos):
            if pos[1] > -1:
                grid[pos[1]][pos[0]] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Tetromino(5, 0)
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetromino(screen, current_piece)

        pygame.draw.rect(screen, WHITE, (GRID_WIDTH * BLOCK_SIZE, 0, 6 * BLOCK_SIZE, SCREEN_HEIGHT))
        score_label = font.render(f'Score: {score}', 1, BLACK)
        screen.blit(score_label, (GRID_WIDTH * BLOCK_SIZE + 10, 20))

        pygame.display.update()

        if not valid_space(current_piece, grid) and current_piece.y < 1:
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()