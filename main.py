#!/usr/bin/python

import pygame
import random
import json
import os
import pygame
# Initialize Pygame
pygame.init()

# Get display information
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Load and play startup jingle
pygame.mixer.music.load("assets/audio/startup_jingle.mp3")
pygame.mixer.music.play()


# Get display information
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

SHIP_SIZE = 50
BULLET_SIZE = 40
ALIEN_SIZE = 30
POWERUP_SIZE = 15
FPS = 60

INITIAL_ALIEN_POPULATION = 5

INCREASE_ALIENS_BY = 1

INCREASE_ALIEN_SPEED_BY = 0.1

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# File to store high scores
SCORE_FILE = "assets/high_scores.json"

def show_startup_screen(screen):
    font = pygame.font.Font(None, 36)
    title_text = font.render("Alien Invasion", True, WHITE)
    controls_text = font.render("Controls: Arrow keys to move, Space to shoot & ESC to Quit", True, WHITE)
    start_text = font.render("Press S to Start", True, WHITE)
    screen.fill((0, 0, 0))
    screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - 100))
    screen.blit(controls_text, (WIDTH / 2 - controls_text.get_width() / 2, HEIGHT / 2 - 50))
    screen.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.pause()
                if event.key == pygame.K_s:
                    waiting = False

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
show_startup_screen(screen)

# Initialize Pygame
#pygame.init()
# Load and play background music
pygame.mixer.music.load("assets/audio/background_music.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
# Ship class
class Ship(pygame.Rect):
    def __init__(self, image):
        super().__init__(WIDTH / 2, HEIGHT - SHIP_SIZE * 2, SHIP_SIZE, SHIP_SIZE)
        self.image = image
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.left > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.right < WIDTH:
            self.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Bullet class
class Bullet(pygame.Rect):
    def __init__(self, x, y, image, speed=10):
        super().__init__(x, y, BULLET_SIZE, BULLET_SIZE)
        self.image = image
        self.speed = speed

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Alien class
class Alien(pygame.Rect):
    def __init__(self, image):
        super().__init__(
            random.randint(0, WIDTH - ALIEN_SIZE), 0, ALIEN_SIZE, ALIEN_SIZE
        )
        self.image = image
        self.speed_x = random.choice([-2, 2])
        self.speed_y = 0.5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.left < 0 or self.right > WIDTH:
            self.speed_x *= -1
        if self.bottom > HEIGHT:
            return False
        return True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Power-up class
class PowerUp(pygame.Rect):
    def __init__(self, image):
        super().__init__(
            random.randint(0, WIDTH - POWERUP_SIZE), 0, POWERUP_SIZE, POWERUP_SIZE
        )
        self.image = image
        self.speed_y = 2

    def move(self):
        self.y += self.speed_y
        if self.top > HEIGHT:
            return False
        return True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    return 0

def save_high_score(score):
    with open(SCORE_FILE, "w") as file:
        json.dump({"high_score": score}, file)

def show_game_over_screen(screen, score, new_high_score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, WHITE)
    high_score_text = font.render(
        "New High Score!" if new_high_score else "Try Again!", True, BLUE
    )
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - 50))
    screen.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 2))
    screen.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, HEIGHT / 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def show_pause_screen(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Paused", True, WHITE)
    continue_text = font.render("Press C to Continue or Q to Quit", True, WHITE)
    screen.fill((0, 0, 0))
    screen.blit(text, (WIDTH / 2 - 100, HEIGHT / 2 - 50))
    screen.blit(continue_text, (WIDTH / 2 - 200, HEIGHT / 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()

    # Load images
    ship_image = pygame.image.load("assets/img/ship.png").convert_alpha()
    bullet_image = pygame.image.load("assets/img/bullet.png").convert_alpha()
    alien_image = pygame.image.load("assets/img/alien.png").convert_alpha()
    powerup_image = pygame.image.load("assets/img/powerup.png").convert_alpha()
    sky_image = pygame.image.load("assets/img/sky.jpg").convert()
    sea_image = pygame.image.load("assets/img/sea.jpg").convert()

    # Resize images
    sky_height = int(HEIGHT * 0.6)
    sea_height = int(HEIGHT * 0.4)
    sky_image = pygame.transform.scale(sky_image, (WIDTH, sky_height))
    sea_image = pygame.transform.scale(sea_image, (WIDTH, sea_height))

    # Game variables
    ship = Ship(ship_image)
    bullets = []
    aliens = [Alien(alien_image) for _ in range(INITIAL_ALIEN_POPULATION)]
    powerups = []
    score = 0
    lives = 3
    level = 1
    high_score = load_high_score()

    # Load sounds
    shoot_sound = pygame.mixer.Sound("assets/audio/shoot.mp3")
    hit_sound = pygame.mixer.Sound("assets/audio/cinema-hit.mp3")
    game_over_sound = pygame.mixer.Sound("assets/audio/game-over.mp3")

    # Shooting control variables
    shoot_delay = 250  # milliseconds
    last_shot_time = pygame.time.get_ticks()

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_pause_screen(screen)

        # Get key presses
        keys = pygame.key.get_pressed()

        # Move ship
        ship.move(keys)

        # Handle shooting
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_shot_time > shoot_delay:
            bullets.append(Bullet(ship.centerx, ship.top, bullet_image))
            shoot_sound.play()
            last_shot_time = current_time

        # Move bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move aliens
        new_aliens = []
        for alien in aliens[:]:
            if not alien.move():
                aliens.remove(alien)
            else:
                new_aliens.append(alien)

        aliens = new_aliens + [
            Alien(alien_image) for _ in range(len(aliens) - len(new_aliens))
        ]

        # Move power-ups
        for powerup in powerups[:]:
            if not powerup.move():
                powerups.remove(powerup)

        # Check collisions
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if bullet.colliderect(alien):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 10
                    hit_sound.play()
                    if random.random() < 0.1:  # 10% chance to drop a power-up
                        powerups.append(PowerUp(powerup_image))

        for powerup in powerups[:]:
            if powerup.colliderect(ship):
                powerups.remove(powerup)
                score += 50  # Example power-up effect

        # Check if all aliens are destroyed
        if not aliens:
            level += 1
            aliens = [Alien(alien_image) for _ in range(INITIAL_ALIEN_POPULATION + level * INCREASE_ALIENS_BY)]
            for alien in aliens:
                alien.speed_y += level * INCREASE_ALIEN_SPEED_BY

        # Check if ship is hit or reaches bottom
        for alien in aliens[:]:
            if alien.colliderect(ship):
                lives -= 1
                ship.centerx = WIDTH / 2
                ship.bottom = HEIGHT - SHIP_SIZE * 2
            if alien.bottom > HEIGHT:
                lives -= 1
                ship.centerx = WIDTH / 2
                ship.bottom = HEIGHT - SHIP_SIZE * 2

        # Game over
        if lives <= 0:
            game_over_sound.play()
            new_high_score = False
            if score > high_score:
                high_score = score
                save_high_score(high_score)
                new_high_score = True
            show_game_over_screen(screen, score, new_high_score)
            return

        # Draw everything
        screen.blit(sky_image, (0, 0))
        screen.blit(sea_image, (0, HEIGHT - sea_height))
        ship.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for alien in aliens:
            alien.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (10, 90))
        screen.blit(high_score_text, (10, 130))

        # Update display
        pygame.display.flip()

        # Cap frame rate
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

# Main loop
while True:
    main()
