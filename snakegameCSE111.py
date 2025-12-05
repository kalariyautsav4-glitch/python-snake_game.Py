#!/usr/bin/env python3
"""
Snake Game (single-file)
Author: Your Name
Description: Classic Snake game using Pygame. Controls: Arrow keys or WASD.
"""

import pygame
import random
import sys

# === Configuration ===
CELL_SIZE = 20         # size of a grid cell in pixels
GRID_WIDTH = 30        # number of cells horizontally
GRID_HEIGHT = 20       # number of cells vertically
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10               # initial frames per second (game speed)
SPEED_INCREMENT_SCORE = 5  # every X points, increase speed by 1 fps

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (200,  30,  30)
GREEN = ( 50, 200,  50)
DARK_GREEN = (20,120,20)
GRAY  = (100, 100, 100)

# === Helper functions ===
def random_food_position(snake):
    """Return a random position (x, y) on grid not occupied by the snake."""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

def draw_cell(surface, pos, color):
    """Draw one grid cell based on grid coordinates (x, y)."""
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)

def draw_grid(surface):
    """Optionally draw grid lines (subtle)."""
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, GRAY, (x*CELL_SIZE, 0), (x*CELL_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY, (0, y*CELL_SIZE), (SCREEN_WIDTH, y*CELL_SIZE))

# === Game initialization ===
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game - Python")
    clock = pygame.time.Clock()

    # Fonts
    font_small = pygame.font.SysFont(None, 24)
    font_big = pygame.font.SysFont(None, 48)

    # Initial snake (center of the screen)
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = (1, 0)  # moving right initially
    next_direction = direction

    food = random_food_position(snake)
    score = 0
    speed = FPS
    running = True
    game_over = False

    while running:
        # === Event handling ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    next_direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_r and game_over:
                    # Restart
                    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
                    direction = (1, 0)
                    next_direction = direction
                    food = random_food_position(snake)
                    score = 0
                    speed = FPS
                    game_over = False

        if not running:
            break

        if not game_over:
            # Prevent reversing directly into itself
            if (next_direction[0] * -1, next_direction[1] * -1) != direction:
                direction = next_direction

            # Move snake: compute new head
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Check wall collisions (wrap-around or die? We'll die on hitting wall)
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                game_over = True

            # Check self-collision
            if new_head in snake:
                game_over = True

            if not game_over:
                snake.insert(0, new_head)  # add new head

                # Check food
                if new_head == food:
                    score += 1
                    # spawn new food not on snake
                    food = random_food_position(snake)
                    # increase speed every few points
                    if score % SPEED_INCREMENT_SCORE == 0:
                        speed += 1
                else:
                    snake.pop()  # remove tail

        # === Drawing ===
        screen.fill(BLACK)

        # Optionally: draw_grid(screen)
        # Draw food
        draw_cell(screen, food, RED)

        # Draw snake (head brighter)
        if snake:
            draw_cell(screen, snake[0], GREEN)
            for segment in snake[1:]:
                draw_cell(screen, segment, DARK_GREEN)

        # Score
        score_surf = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (8, 8))

        # Game over screen
        if game_over:
            over_surf = font_big.render("GAME OVER", True, RED)
            rect = over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 24))
            screen.blit(over_surf, rect)

            info_surf = font_small.render("Press R to Restart or ESC to Quit", True, WHITE)
            rect2 = info_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 16))
            screen.blit(info_surf, rect2)

            final_score = font_small.render(f"Final Score: {score}", True, WHITE)
            rect3 = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 44))
            screen.blit(final_score, rect3)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
