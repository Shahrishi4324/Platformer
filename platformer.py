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
pygame.display.set_caption("2D Platformer - Step 3")

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

# Enemy settings
enemy_size = 50
enemy_color = (255, 0, 0)
enemies = [
    {'rect': pygame.Rect(200, 450, enemy_size, enemy_size), 'dir': 1},
    {'rect': pygame.Rect(100, 300, enemy_size, enemy_size), 'dir': -1},
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

    # Enemy movement and collision
    for enemy in enemies:
        enemy['rect'].x += 3 * enemy['dir']
        if enemy['rect'].left < 0 or enemy['rect'].right > WIDTH:
            enemy['dir'] *= -1

        if player_rect.colliderect(enemy['rect']):
            print("Player hit! Game Over!")
            pygame.quit()
            sys.exit()

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, player_color, player_rect)
    for platform in platforms:
        pygame.draw.rect(screen, platform_color, platform)
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, enemy['rect'])

    # Update display
    pygame.display.flip()
    clock.tick(FPS)