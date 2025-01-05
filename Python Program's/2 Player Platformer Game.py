import pygame
import random
import json
from pygame.locals import *

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Platformer")

# Player, Enemy, Tile, and Power-up setup
class Character:
    def __init__(self, name, speed, jump_height, color, start_pos):
        self.name = name
        self.speed = speed
        self.jump_height = jump_height
        self.color = color
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 30, 50)
        self.vel_y = 0
        self.is_jumping = False

    def move(self, keys, up, left, right):
        if keys[up] and not self.is_jumping:
            self.vel_y = -self.jump_height
            self.is_jumping = True
        if keys[left]: self.rect.x -= self.speed
        if keys[right]: self.rect.x += self.speed
        self.rect.y += self.vel_y
        self.vel_y += 1  # Gravity effect
        if self.rect.y >= HEIGHT - 50:  # Ground collision
            self.rect.y = HEIGHT - 50
            self.vel_y = 0
            self.is_jumping = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(2, 5)

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1  # Change direction at screen edges

    def draw(self):
        pygame.draw.rect(screen, (200, 0, 0), self.rect)

class Tile:
    def __init__(self, x, y, type=1):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.type = type  # 1 for platform, 0 for empty

    def draw(self):
        color = (100, 100, 100) if self.type == 1 else (200, 200, 200)
        pygame.draw.rect(screen, color, self.rect)

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.active = True

    def apply(self, character):
        character.speed += 2

# Game functions
tiles = []
enemies = []
power_ups = []
players = [
    Character("Speedy", 7, 15, (255, 0, 0), (100, HEIGHT - 50)),
    Character("Jumper", 5, 20, (0, 0, 255), (200, HEIGHT - 50))
]

def draw_grid():
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (180, 180, 180), rect, 1)

def save_level(filename="level.json"):
    level_data = [{"x": tile.rect.x, "y": tile.rect.y, "type": tile.type} for tile in tiles]
    with open(filename, "w") as f:
        json.dump(level_data, f)

def load_level(filename="level.json"):
    with open(filename, "r") as f:
        level_data = json.load(f)
        tiles.clear()
        for data in level_data:
            tiles.append(Tile(data["x"], data["y"], data["type"]))

def generate_level():
    tiles.clear()
    enemies.clear()
    for _ in range(10):  # Random platforms
        x = random.randint(0, WIDTH - GRID_SIZE)
        y = random.randint(GRID_SIZE, HEIGHT - GRID_SIZE)
        tiles.append(Tile(x, y, 1))
    for _ in range(3):  # Random enemies
        x = random.randint(0, WIDTH - 30)
        y = random.randint(0, HEIGHT - 50)
        enemies.append(Enemy(x, y))

def draw_level():
    for tile in tiles:
        tile.draw()
    for enemy in enemies:
        enemy.draw()
    for power_up in power_ups:
        if power_up.active:
            pygame.draw.rect(screen, (0, 255, 0), power_up.rect)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))
    draw_grid()
    keys = pygame.key.get_pressed()

    # Player actions
    players[0].move(keys, K_w, K_a, K_d)
    players[1].move(keys, K_UP, K_LEFT, K_RIGHT)

    # Enemy movement and collision
    for enemy in enemies:
        enemy.move()
        for player in players:
            if player.rect.colliderect(enemy.rect):
                print(f"{player.name} collided with an enemy!")

    # Draw everything
    draw_level()
    for player in players:
        player.draw()

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_g:  # Generate new level
                generate_level()
            elif event.key == K_s:  # Save level
                save_level()
            elif event.key == K_l:  # Load level
                load_level()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
