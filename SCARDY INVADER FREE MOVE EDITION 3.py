import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = WHITE  # White for player
LASER_COLOR = WHITE   # White for lasers
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 30
LASER_WIDTH = 5
LASER_HEIGHT = 20
TURTLE_SPEED = 4  # Increased speed for turtles

# Rainbow colors
RAINBOW_COLORS = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211)   # Violet
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SPACE INVADER SCARDY VERSION FREE MOVE EDITION 3')

# Font for displaying score
font = pygame.font.Font(None, 36)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.lives = 3  # Player starts with 3 lives
        self.hits_taken = 0  # Track hits taken

    def update(self):
        if not game_over:  # Only allow movement if the game is not over
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.top > 0:  # Move up
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:  # Move down
                self.rect.y += self.speed

    def shoot(self):
        return Laser(self.rect.centerx, self.rect.top)

class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))  # Same size as player
        self.image.fill(random.choice(RAINBOW_COLORS))  # Assign a random rainbow color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += TURTLE_SPEED  # Move downwards
        if self.rect.top >= SCREEN_HEIGHT:  # If it goes off screen, respawn at the top
            self.rect.y = random.randint(-150, -30)
            self.rect.x = random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH)  # Adjusted for new width

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
        self.image.fill(LASER_COLOR)  # White color for lasers
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Function to reset the game
def reset_game():
    global player, score, turtles, all_sprites, lasers, game_over
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    turtles = pygame.sprite.Group()
    lasers = pygame.sprite.Group()  # Define lasers group here
    score = 0
    game_over = False  # Reset game over status

    # Spawn initial turtles
    for _ in range(5):  # Start with 5 turtles
        spawn_turtle()

# Function to spawn turtles at random positions
def spawn_turtle():
    x = random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH)  # Adjusted for new width
    y = random.randint(-150, -30)  # Start turtles above the screen
    turtle = Turtle(x, y)
    all_sprites.add(turtle)
    turtles.add(turtle)

# Game loop
running = True
clock = pygame.time.Clock()
reset_game()

# Restart button setup
button_font = pygame.font.Font(None, 48)
restart_button = None
game_over = False  # Track game over state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                laser = player.shoot()
                all_sprites.add(laser)
                lasers.add(laser)  # Add laser to the lasers group
        elif event.type == pygame.MOUSEBUTTONDOWN and restart_button and restart_button.collidepoint(event.pos):
            reset_game()  # Reset game on button click

    # Update all sprites
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(lasers, turtles, True, True)
    if hits:
        for _ in hits:
            spawn_turtle()  # Respawn a turtle for each one that was hit
            score += 1  # Increase score for each hit

    # Check for collisions with player
    if pygame.sprite.spritecollide(player, turtles, False):
        player.hits_taken += 1  # Increase hits taken
        if player.hits_taken >= 3:  # If hits taken reaches 3
            player.lives -= 1  # Decrease lives
            player.hits_taken = 0  # Reset hits taken after losing a life
            if player.lives <= 0:
                print("Game Over!")  # End game logic
                game_over = True  # Set game over status
                restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw the score
    score_text = font.render(f"Punti Attuali: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))  # Top right corner

    # Draw restart button if game is over
    if game_over:
        pygame.draw.rect(screen, (255, 0, 0), restart_button)  # Draw button in red
        restart_text = button_font.render("Restart", True, WHITE)
        screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
