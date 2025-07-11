import pygame
from classes.grid import Grid, Resource
from classes.cursor import Cursor
from classes.unit import Unit
from classes.overlay import UnitOverlay
from classes.unitpath import UnitPath
from classes.gameboard import GameBoard

pygame.init()

TILE_SIZE = 40
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

board = GameBoard()

def draw_grid():
    for y in range(board.grid.height):
        for x in range(board.grid.width):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (70, 70, 70), rect, 1)

def draw_cursor():
    rect = pygame.Rect(board.cursor.x * TILE_SIZE, board.cursor.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (255, 255, 0), rect, 3)

def draw_units():
    for unit in board.units:
        color = (0, 200, 255) if unit.team == "player" else (255, 60, 60)
        if unit == board.get_active_unit():
            color = (0, 255, 0)
        rect = pygame.Rect(unit.x * TILE_SIZE + 6, unit.y * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12)
        pygame.draw.rect(screen, color, rect)
        # Draw HP as text
        font = pygame.font.SysFont(None, 20)
        hp_text = font.render(str(unit.hp), True, (255, 255, 255))
        screen.blit(hp_text, (unit.x * TILE_SIZE + 10, unit.y * TILE_SIZE + 10))

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            board.handle_input(event.key)

    board.update()

    draw_grid()
    draw_units()
    draw_cursor()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
