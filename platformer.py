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
pygame.display.set_caption("2D Platformer - Step 4")

# Player settings
player_size = 50
player_color = (0, 128, 255)
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_vel_x = 5
player_vel_y = 0
player_jump = False
gravity = 0.5
lives = 3
score = 0

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

# Power-ups and collectibles
powerup_size = 30
coin_size = 20
powerup_color = (255, 215, 0)
coin_color = (255, 223, 0)

powerups = [
    {'rect': pygame.Rect(600, 470, powerup_size, powerup_size), 'type': 'extra_life'},
    {'rect': pygame.Rect(150, 320, powerup_size, powerup_size), 'type': 'speed_boost'}
]

coins = [
    pygame.Rect(250, 470, coin_size, coin_size),
    pygame.Rect(200, 320, coin_size, coin_size),
    pygame.Rect(550, 170, coin_size, coin_size),
]

# Game loop
clock = pygame.time.Clock()
speed_boost_active = False
speed_boost_timer = 0

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
            lives -= 1
            print(f"Player hit! Lives remaining: {lives}")
            if lives <= 0:
                print("Game Over!")
                pygame.quit()
                sys.exit()

    # Power-up interaction
    for powerup in powerups[:]:
        if player_rect.colliderect(powerup['rect']):
            if powerup['type'] == 'extra_life':
                lives += 1
                print(f"Extra Life! Lives: {lives}")
            elif powerup['type'] == 'speed_boost':
                speed_boost_active = True
                player_vel_x *= 2
                speed_boost_timer = pygame.time.get_ticks()
                print("Speed Boost Activated!")
            powerups.remove(powerup)

    # Speed boost duration
    if speed_boost_active:
        if pygame.time.get_ticks() - speed_boost_timer > 5000:  # 5-second duration
            speed_boost_active = False
            player_vel_x /= 2
            print("Speed Boost Ended")

    # Coin collection
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            score += 10
            print(f"Coin collected! Score: {score}")
            coins.remove(coin)

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, player_color, player_rect)
    for platform in platforms:
        pygame.draw.rect(screen, platform_color, platform)
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, enemy['rect'])
    for powerup in powerups:
        pygame.draw.rect(screen, powerup_color, powerup['rect'])
    for coin in coins:
        pygame.draw.rect(screen, coin_color, coin)

    # Display player stats
    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)