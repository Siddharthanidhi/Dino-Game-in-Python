import pygame # type: ignore
import random
import sys
import os
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Sprite Game - Upgraded")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 36)

# Load sprite sequences
def load_sprite_sequence(folder, prefix, count, size):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join(folder, f"{prefix}_{i}.png")
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        frames.append(img)
    return frames

# Assets
ASSETS = "assets"
DINO_DIR = os.path.join(ASSETS, "dino")
GROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "ground.png")), (800, 20))
CLOUD_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "cloud.png")), (60, 30))
CACTUS_IMG = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "cactus.png")), (40, 60))

# Dino Animations
RUN_FRAMES = load_sprite_sequence(os.path.join(DINO_DIR, "run"), "Run", 8, (60, 60))
JUMP_FRAMES = load_sprite_sequence(os.path.join(DINO_DIR, "jump"), "Jump", 12, (60, 60))
IDLE_FRAMES = load_sprite_sequence(os.path.join(DINO_DIR, "idle"), "Idle", 10, (60, 60))
DEAD_FRAMES = load_sprite_sequence(os.path.join(DINO_DIR, "dead"), "Dead", 8, (60, 60))

# Dino State
dino_x = 100
dino_y = 300
dino_vel_y = 0
gravity = 1
frame_index = 0
frame_timer = 0
DINO_RECT = pygame.Rect(dino_x, dino_y, 60, 60)

# Game State
jumping = False
dead = False
idle = False
last_input_time = time.time()
game_over = False

# Obstacle
obstacle = pygame.Rect(WIDTH, 300, 40, 60)

# Cloud
cloud_x = WIDTH
cloud_y = 50

# Ground scroll
ground_x = 0

# Score
score = 0
high_score = 0

# Restart function
def reset_game():
    global dino_y, dino_vel_y, jumping, dead, idle, frame_index, frame_timer
    global obstacle, score, cloud_x, cloud_y, ground_x, game_over
    dino_y = 300
    dino_vel_y = 0
    jumping = False
    dead = False
    idle = False
    frame_index = 0
    frame_timer = 0
    obstacle.x = WIDTH
    score = 0
    cloud_x = WIDTH
    cloud_y = 50
    ground_x = 0
    game_over = False

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))

    current_time = time.time()
    if not dead:
        idle = (current_time - last_input_time > 5 and not jumping)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        reset_game()
        continue

    if keys[pygame.K_SPACE] and not jumping and not dead:
        dino_vel_y = -16
        jumping = True
        last_input_time = current_time

    # Physics
    if not dead:
        dino_vel_y += gravity
        dino_y += dino_vel_y
        if dino_y >= 300:
            dino_y = 300
            jumping = False
        DINO_RECT.topleft = (dino_x, dino_y)

    # Animation timing
    frame_timer += 1
    if frame_timer >= 6:
        frame_index += 1
        frame_timer = 0

    # Ground & background
    if not dead:
        obstacle.x -= 8
        cloud_x -= 2
        ground_x -= 8

        if cloud_x < -60:
            cloud_x = WIDTH + random.randint(0, 100)
            cloud_y = random.randint(20, 100)

        if ground_x <= -800:
            ground_x = 0

    # Reset obstacle if off-screen
    if obstacle.right < 0 and not dead:
        obstacle.x = WIDTH + random.randint(200, 500)
        score += 1

    # Collision detection
    if DINO_RECT.colliderect(obstacle) and not dead:
        dead = True
        game_over = True
        if score > high_score:
            high_score = score
        frame_index = 0
        frame_timer = 0

    # Draw background
    screen.blit(CLOUD_IMG, (cloud_x, cloud_y))
    screen.blit(GROUND_IMG, (ground_x, 360))
    screen.blit(GROUND_IMG, (ground_x + 800, 360))
    screen.blit(CACTUS_IMG, obstacle.topleft)

    # Draw Dino
    if dead:
        frame_index %= len(DEAD_FRAMES)
        screen.blit(DEAD_FRAMES[frame_index], (dino_x, dino_y))
    elif jumping:
        frame_index %= len(JUMP_FRAMES)
        screen.blit(JUMP_FRAMES[frame_index], (dino_x, dino_y))
    elif idle:
        frame_index %= len(IDLE_FRAMES)
        screen.blit(IDLE_FRAMES[frame_index], (dino_x, dino_y))
    else:
        frame_index %= len(RUN_FRAMES)
        screen.blit(RUN_FRAMES[frame_index], (dino_x, dino_y))

    # Score display
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

    # Game over message
    if game_over:
        game_over_text = FONT.render("Game Over! Press R to Restart", True, (200, 0, 0))
        screen.blit(game_over_text, (WIDTH//2 - 160, HEIGHT//2 - 20))

    pygame.display.update()
    clock.tick(60)

