import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Enhanced Features")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)

# Font
font = pygame.font.SysFont(None, 50)

# Player settings
player_size = 50
player1_start_pos = [WIDTH // 4, HEIGHT - player_size - 10]
player2_start_pos = [3 * WIDTH // 4, HEIGHT - player_size - 10]
player1_pos = list(player1_start_pos)
player2_pos = list(player2_start_pos)
normal_velocity = 5
sprint_velocity = 8
jump_strength = 15
gravity = 1
max_health = 3

# Player states
is_jumping_1 = False
double_jump_used_1 = False
triple_jump_used_1 = False
y_velocity_1 = 0
health_1 = max_health

is_jumping_2 = False
double_jump_used_2 = False
triple_jump_used_2 = False
y_velocity_2 = 0
health_2 = max_health

coins_collected = 0

# Power-ups
power_up_costs = {
    "Super Jump": 5,
    "Flying": 10,
    "Speed Boost": 7,
    "Shield": 8,
    "Double Coins": 12,
    "Low Gravity": 8,
    "Invincibility": 15,
    "Triple Jump": 10,
    "Score Multiplier": 12
}
active_power_ups = {power_up: False for power_up in power_up_costs}
power_up_durations = {"Flying": 10, "Speed Boost": 5, "Shield": 8, "Double Coins": 10, "Low Gravity": 8, "Invincibility": 10, "Score Multiplier": 10}
power_up_start_times = {}

# Platform settings
platforms = []
coin_pos = (WIDTH - 100, HEIGHT - 150)  # Starting position of the coin
min_distance = 300  # Minimum distance for coin placement from the player

# Enemy settings
enemy_size = 30
enemies = []  # List to store enemies

# Obstacle settings
obstacles = []  # List to store obstacles (like spikes)
obstacle_size = 20

# Portal settings
portals = []  # List to store pairs of portals
portal_size = 30

# Health Pack settings
health_packs = []

# Game variables
win = False
game_state = "menu"  # Possible states: "menu", "playing", "game_over", "win", "shop"

# Function to render text
def render_text(text, size, color, position):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Function to generate a new level
def generate_level():
    global platforms, coin_pos, enemies, obstacles, portals, health_packs
    platforms = [
        pygame.Rect(100, HEIGHT - 50, 200, 10),
        pygame.Rect(400, HEIGHT - 150, 200, 10),
        pygame.Rect(200, HEIGHT - 250, 200, 10),
        pygame.Rect(600, HEIGHT - 350, 200, 10),
        pygame.Rect(0, HEIGHT - 10, WIDTH, 10),  # Ground platform
    ]
    # Randomize coin position, ensuring it is far from the player start positions
    while True:
        coin_x = random.randint(100, WIDTH - 100)
        coin_y = random.randint(300, HEIGHT - 200)  # Lower coin placement
        distance_1 = math.sqrt((coin_x - player1_start_pos[0]) ** 2 + (coin_y - player1_start_pos[1]) ** 2)
        distance_2 = math.sqrt((coin_x - player2_start_pos[0]) ** 2 + (coin_y - player2_start_pos[1]) ** 2)
        if distance_1 >= min_distance and distance_2 >= min_distance:
            coin_pos = (coin_x, coin_y)
            break

    # Generate enemies on random platforms
    enemies = []
    for platform in platforms[:-1]:  # Skip the ground platform for enemies
        if random.random() < 0.5:  # 50% chance to spawn an enemy on each platform
            enemy_x = platform.x + random.randint(0, platform.width - enemy_size)
            enemy_y = platform.y - enemy_size
            enemy_speed = random.choice([-1, 1]) * random.randint(1, 3)
            enemies.append({'rect': pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size), 'speed': enemy_speed})

    # Generate obstacles (spikes) on platforms
    obstacles = []
    for platform in platforms[:-1]:
        if random.random() < 0.5:  # 50% chance to place a spike
            obs_x = platform.x + random.randint(0, platform.width - obstacle_size)
            obs_y = platform.y - obstacle_size
            obstacles.append(pygame.Rect(obs_x, obs_y, obstacle_size, obstacle_size))

    # Generate portals in pairs
    portals = []
    if len(platforms) > 2:
        for _ in range(2):  # Two pairs of portals
            portal1_x = platforms[0].x + random.randint(0, platforms[0].width - portal_size)
            portal1_y = platforms[0].y - portal_size
            portal2_x = platforms[-2].x + random.randint(0, platforms[-2].width - portal_size)
            portal2_y = platforms[-2].y - portal_size
            portals.append((pygame.Rect(portal1_x, portal1_y, portal_size, portal_size), pygame.Rect(portal2_x, portal2_y, portal_size, portal_size)))

    # Generate health packs randomly on platforms
    health_packs = []
    for platform in platforms[:-1]:
        if random.random() < 0.3:  # 30% chance for a health pack
            hp_x = platform.x + random.randint(0, platform.width - 20)
            hp_y = platform.y - 20
            health_packs.append(pygame.Rect(hp_x, hp_y, 20, 20))

# Initialize the first level
generate_level()

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    current_time = time.time()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_state == "menu":
                    game_state = "playing"
                    player1_pos = list(player1_start_pos)  # Reset player 1 position
                    player2_pos = list(player2_start_pos)  # Reset player 2 position
                elif game_state == "shop":
                    game_state = "playing"  # Return to game
                elif game_state == "win" or game_state == "game_over":
                    # Reset game
                    game_state = "menu"
                    player1_pos = list(player1_start_pos)
                    player2_pos = list(player2_start_pos)
                    is_jumping_1 = is_jumping_2 = False
                    double_jump_used_1 = double_jump_used_2 = False
                    triple_jump_used_1 = triple_jump_used_2 = False
                    y_velocity_1 = y_velocity_2 = 0
                    health_1 = health_2 = max_health
                    win = False
            elif event.key == pygame.K_s and game_state == "playing":
                game_state = "shop"  # Open the shop
            elif game_state == "shop":
                # Power-Up purchases
                power_up_keys = list(power_up_costs.keys())
                for i, power_up in enumerate(power_up_keys):
                    if event.key == pygame.K_1 + i and coins_collected >= power_up_costs[power_up]:
                        coins_collected -= power_up_costs[power_up]
                        active_power_ups[power_up] = True
                        if power_up in power_up_durations:
                            power_up_start_times[power_up] = current_time

    # Game States
    if game_state == "menu":
        render_text("Press Enter to Start", 50, BLACK, (WIDTH // 2 - 150, HEIGHT // 2))
        render_text("Press 'S' in-game to open the Shop", 30, BLACK, (WIDTH // 2 - 150, HEIGHT // 2 + 60))
    elif game_state == "playing":
        # Apply active power-ups
        if active_power_ups["Super Jump"]:
            jump_strength = 25
        else:
            jump_strength = 15

        if active_power_ups["Low Gravity"]:
            gravity = 0.5
        else:
            gravity = 1

        if active_power_ups["Flying"] and current_time - power_up_start_times.get("Flying", 0) <= power_up_durations["Flying"]:
            y_velocity_1 = y_velocity_2 = 0  # Both players can fly

        # Player 1 movement (WASD)
        keys = pygame.key.get_pressed()
        player1_velocity = sprint_velocity if keys[pygame.K_LSHIFT] else normal_velocity
        if keys[pygame.K_a] and player1_pos[0] > 0:
            player1_pos[0] -= player1_velocity
        if keys[pygame.K_d] and player1_pos[0] < WIDTH - player_size:
            player1_pos[0] += player1_velocity
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and not is_jumping_1:
            is_jumping_1 = True
            y_velocity_1 = -jump_strength
        elif keys[pygame.K_w] and is_jumping_1 and not double_jump_used_1:
            y_velocity_1 = -jump_strength
            double_jump_used_1 = True
        elif keys[pygame.K_w] and double_jump_used_1 and active_power_ups["Triple Jump"] and not triple_jump_used_1:
            y_velocity_1 = -jump_strength
            triple_jump_used_1 = True

        # Player 2 movement (Arrow Keys)
        player2_velocity = sprint_velocity if keys[pygame.K_RSHIFT] else normal_velocity
        if keys[pygame.K_LEFT] and player2_pos[0] > 0:
            player2_pos[0] -= player2_velocity
        if keys[pygame.K_RIGHT] and player2_pos[0] < WIDTH - player_size:
            player2_pos[0] += player2_velocity
        if keys[pygame.K_UP] and not is_jumping_2:
            is_jumping_2 = True
            y_velocity_2 = -jump_strength
        elif keys[pygame.K_UP] and is_jumping_2 and not double_jump_used_2:
            y_velocity_2 = -jump_strength
            double_jump_used_2 = True
        elif keys[pygame.K_UP] and double_jump_used_2 and active_power_ups["Triple Jump"] and not triple_jump_used_2:
            y_velocity_2 = -jump_strength
            triple_jump_used_2 = True

        # Apply gravity and jumping for Player 1
        y_velocity_1 += gravity
        player1_pos[1] += y_velocity_1
        player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], player_size, player_size)
        for platform in platforms:
            if player1_rect.colliderect(platform) and y_velocity_1 >= 0:
                player1_pos[1] = platform.y - player_size
                is_jumping_1 = False
                double_jump_used_1 = False
                triple_jump_used_1 = False
                y_velocity_1 = 0

        # Apply gravity and jumping for Player 2
        y_velocity_2 += gravity
        player2_pos[1] += y_velocity_2
        player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], player_size, player_size)
        for platform in platforms:
            if player2_rect.colliderect(platform) and y_velocity_2 >= 0:
                player2_pos[1] = platform.y - player_size
                is_jumping_2 = False
                double_jump_used_2 = False
                triple_jump_used_2 = False
                y_velocity_2 = 0

        # Check if players collect the coin
        coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], 30, 30)
        if player1_rect.colliderect(coin_rect) or player2_rect.colliderect(coin_rect):
            coins_collected += 2 if active_power_ups["Double Coins"] else 1
            generate_level()
            player1_pos = list(player1_start_pos)
            player2_pos = list(player2_start_pos)

        # If either player falls off screen
        if player1_pos[1] > HEIGHT:
            health_1 -= 1
            player1_pos = list(player1_start_pos)
            if health_1 <= 0:
                game_state = "game_over"
        if player2_pos[1] > HEIGHT:
            health_2 -= 1
            player2_pos = list(player2_start_pos)
            if health_2 <= 0:
                game_state = "game_over"

        # Enemy movement and collision
        for enemy in enemies:
            enemy['rect'].x += enemy['speed']
            if enemy['rect'].left < 0 or enemy['rect'].right > WIDTH:
                enemy['speed'] *= -1  # Reverse direction if enemy hits screen edge
            if player1_rect.colliderect(enemy['rect']):
                health_1 -= 1
                if health_1 <= 0:
                    game_state = "game_over"
            if player2_rect.colliderect(enemy['rect']):
                health_2 -= 1
                if health_2 <= 0:
                    game_state = "game_over"

        # Obstacle collision
        for obstacle in obstacles:
            if player1_rect.colliderect(obstacle):
                health_1 -= 1
                if health_1 <= 0:
                    game_state = "game_over"
            if player2_rect.colliderect(obstacle):
                health_2 -= 1
                if health_2 <= 0:
                    game_state = "game_over"

        # Portal collision
        for portal1, portal2 in portals:
            if player1_rect.colliderect(portal1):
                player1_pos = [portal2.x, portal2.y - player_size]
            elif player1_rect.colliderect(portal2):
                player1_pos = [portal1.x, portal1.y - player_size]
            if player2_rect.colliderect(portal1):
                player2_pos = [portal2.x, portal2.y - player_size]
            elif player2_rect.colliderect(portal2):
                player2_pos = [portal1.x, portal1.y - player_size]

        # Health pack collision
        for hp in health_packs[:]:
            if player1_rect.colliderect(hp):
                health_1 = min(health_1 + 1, max_health)
                health_packs.remove(hp)
            elif player2_rect.colliderect(hp):
                health_2 = min(health_2 + 1, max_health)
                health_packs.remove(hp)

        # Draw platforms, players, and other objects
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)
        pygame.draw.rect(screen, BLUE, player1_rect)  # Player 1
        pygame.draw.rect(screen, RED, player2_rect)   # Player 2
        for enemy in enemies:
            pygame.draw.rect(screen, YELLOW, enemy['rect'])
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)
        for portal1, portal2 in portals:
            pygame.draw.rect(screen, PURPLE, portal1)
            pygame.draw.rect(screen, PURPLE, portal2)
        for hp in health_packs:
            pygame.draw.rect(screen, BLUE, hp)
        pygame.draw.circle(screen, GOLD, coin_pos, 15)

        # Display coins, health, etc.
        render_text(f"Coins: {coins_collected}", 30, BLACK, (10, 10))
        render_text(f"Player 1 Health: {health_1}", 30, BLACK, (10, 40))
        render_text(f"Player 2 Health: {health_2}", 30, BLACK, (10, 70))

    elif game_state == "shop":
        screen.fill(WHITE)
        render_text("Shop - Press 1 to 9 to Buy Power-Ups", 30, BLACK, (WIDTH // 2 - 200, 50))
        for i, power_up in enumerate(power_up_costs):
            render_text(f"{i+1}. {power_up} ({power_up_costs[power_up]} Coins)", 25, BLACK, (100, 150 + i * 40))
        render_text("Press Enter to return to game", 25, BLACK, (WIDTH // 2 - 150, HEIGHT - 50))

    elif game_state == "game_over":
        render_text("Game Over! Press Enter to Restart", 40, RED, (WIDTH // 2 - 220, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
