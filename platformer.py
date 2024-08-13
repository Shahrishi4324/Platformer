import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer - Step 1")

# Player settings
player_size = 50
player_color = (0, 128, 255)
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_vel_x = 5
player_vel_y = 0
player_jump = False
gravity = 0.5

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_vel_x
    if keys[pygame.K_RIGHT]:
        player_x += player_vel_x
    if keys[pygame.K_SPACE] and not player_jump:
        player_vel_y = -10
        player_jump = True

    # Apply gravity
    player_vel_y += gravity
    player_y += player_vel_y

    # Ground collision
    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_jump = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)