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
pygame.display.set_caption("2D Platformer - Step 2")

# Player settings
player_size = 50
player_color = (0, 128, 255)
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_vel_x = 5
player_vel_y = 0
player_jump = False
gravity = 0.5

# Platform settings
platform_color = (0, 255, 0)
platforms = [
    pygame.Rect(200, 500, 400, 20),
    pygame.Rect(100, 350, 200, 20),
    pygame.Rect(500, 200, 300, 20)
]

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

    # Platform collision
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for platform in platforms:
        if player_rect.colliderect(platform) and player_vel_y > 0:
            player_y = platform.y - player_size
            player_vel_y = 0
            player_jump = False

    # Ground collision
    if player_y >= HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_jump = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, player_color, player_rect)
    for platform in platforms:
        pygame.draw.rect(screen, platform_color, platform)

    # Update display
    pygame.display.flip()
    clock.tick(FPS)