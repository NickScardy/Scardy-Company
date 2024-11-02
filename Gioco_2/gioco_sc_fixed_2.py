import pygame
import random

# Initialize Pygame
pygame.init()

# Game constantsimport pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURTLE_COLOR = (255, 0, 0)  # Red for turtles
BOSS_COLOR = (139, 0, 0)    # Dark red for boss
TURTLE_WIDTH = 50
TURTLE_HEIGHT = 30
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 30
LASER_WIDTH = 5
LASER_HEIGHT = 20
NUM_TURTLES = 5
NUM_WAVES = 10
BOSS_HEALTH = 3
TURTLE_HEALTH = 1

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SPACE INVADER SCARDY VERSION iMac Edition')

# Font for text
font = pygame.font.Font(None, 74)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Laser(self.rect.centerx, self.rect.top)

class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TURTLE_WIDTH, TURTLE_HEIGHT))
        self.image.fill(TURTLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = TURTLE_HEALTH

    def update(self):
        # Movement logic for Turtle
        self.rect.x += random.choice([-1, 1])
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - TURTLE_WIDTH:
            self.rect.x -= random.choice([-1, 1])

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TURTLE_WIDTH, TURTLE_HEIGHT))
        self.image.fill(BOSS_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = 50
        self.health = BOSS_HEALTH

    def update(self):
        # Movement logic for Boss
        self.rect.x += random.choice([-1, 1])
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x -= random.choice([-5, 5])

# Sprite groups
all_sprites = pygame.sprite.Group()
turtles = pygame.sprite.Group()
lasers = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

# Player initialization
player = Player()
all_sprites.add(player)

# Turtle initialization
def spawn_turtles():
    for i in range(NUM_TURTLES):
        x = random.randint(0, SCREEN_WIDTH - TURTLE_WIDTH)
#        y = random.randint(50, 200)
        y = 50
        turtle = Turtle(x, y)
        all_sprites.add(turtle)
        turtles.add(turtle)

spawn_turtles()

# Game loop
running = True
wave = 1
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser = player.shoot()
                all_sprites.add(laser)
                lasers.add(laser)

    # Update all sprites without arguments
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(lasers, turtles, True, True)
    
    if hits:
        if len(turtles) == 0:
            wave += 1
            if wave % NUM_WAVES == 0:
                boss = Boss()
                all_sprites.add(boss)
                boss_group.add(boss)
            else:
                spawn_turtles()
    
    # Check laser collisions with the boss
    boss_hits = pygame.sprite.groupcollide(lasers, boss_group, True, False)
    for hit in boss_hits:
        for boss in boss_group:
            boss.health -= 1
            if boss.health <= 0:
                boss.kill()
                # Reset game state
                wave = 1
                all_sprites.empty()
                lasers.empty()
                turtles.empty()
                boss_group.empty()
                # Reinitialize player and initial wave of turtles
                player = Player()
                all_sprites.add(player)
                spawn_turtles()
                

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
    

    

pygame.quit()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURTLE_COLOR = (255, 0, 0)  # Red for turtles
BOSS_COLOR = (139, 0, 0)    # Dark red for boss
TURTLE_WIDTH = 50
TURTLE_HEIGHT = 30
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 30
LASER_WIDTH = 5
LASER_HEIGHT = 20
NUM_TURTLES = 5
NUM_WAVES = 10
BOSS_HEALTH = 3
TURTLE_HEALTH = 1

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SPACE INVADER SCARDY VERSION iMac Edition')

# Font for text
font = pygame.font.Font(None, 74)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Laser(self.rect.centerx, self.rect.top)

class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TURTLE_WIDTH, TURTLE_HEIGHT))
        self.image.fill(TURTLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = TURTLE_HEALTH

    def update(self):
        # Movement logic for Turtle
        self.rect.x += random.choice([-1, 1])
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - TURTLE_WIDTH:
            self.rect.x -= random.choice([-1, 1])

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TURTLE_WIDTH, TURTLE_HEIGHT))
        self.image.fill(BOSS_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = 50
        self.health = BOSS_HEALTH

    def update(self):
        # Movement logic for Boss
        self.rect.x += random.choice([-1, 1])
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x -= random.choice([-5, 5])

# Sprite groups
all_sprites = pygame.sprite.Group()
turtles = pygame.sprite.Group()
lasers = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

# Player initialization
player = Player()
all_sprites.add(player)

# Turtle initialization
def spawn_turtles():
    for i in range(NUM_TURTLES):
        x = random.randint(0, SCREEN_WIDTH - TURTLE_WIDTH)
#        y = random.randint(50, 200)
        y = 50
        turtle = Turtle(x, y)
        all_sprites.add(turtle)
        turtles.add(turtle)

spawn_turtles()

# Game loop
running = True
wave = 1
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser = player.shoot()
                all_sprites.add(laser)
                lasers.add(laser)

    # Update all sprites without arguments
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(lasers, turtles, True, True)
    
    if hits:
        if len(turtles) == 0:
            wave += 1
            if wave % NUM_WAVES == 0:
                boss = Boss()
                all_sprites.add(boss)
                boss_group.add(boss)
            else:
                spawn_turtles()
    
    # Check laser collisions with the boss
    boss_hits = pygame.sprite.groupcollide(lasers, boss_group, True, False)
    for hit in boss_hits:
        for boss in boss_group:
            boss.health -= 1
            if boss.health <= 0:
                boss.kill()
                # Reset game state
                wave = 1
                all_sprites.empty()
                lasers.empty()
                turtles.empty()
                boss_group.empty()
                # Reinitialize player and initial wave of turtles
                player = Player()
                all_sprites.add(player)
                spawn_turtles()
                

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
    

    

pygame.quit()
