import pygame
import tkinter as tk
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pseudo-3D Runner Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Game variables
LANE_WIDTH = WIDTH // 3
player_pos = 1  # Start in the middle lane (0 = left, 1 = middle, 2 = right)
player_y = HEIGHT - 150
player_size = 50
speed = 5
obstacle_speed = 5
score = 0

# Obstacle and coin lists
obstacles = []
coins = []

# Initialize Tkinter for score display
root = tk.Tk()
root.title("Score")
score_label = tk.Label(root, text=f"Score: {score}", font=("Helvetica", 16))
score_label.pack()


# Helper functions
def spawn_obstacle():
    lane = random.randint(0, 2)
    x_pos = LANE_WIDTH * lane + LANE_WIDTH // 2
    obstacles.append({"x": x_pos, "y": -100, "size": 20, "speed": obstacle_speed})


def spawn_coin():
    lane = random.randint(0, 2)
    x_pos = LANE_WIDTH * lane + LANE_WIDTH // 2
    coins.append({"x": x_pos, "y": -100, "size": 15, "speed": obstacle_speed})


# Game loop
clock = pygame.time.Clock()
spawn_timer = 0
running = True

while running:
    screen.fill(GRAY)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            root.destroy()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_pos > 0:
                player_pos -= 1
            elif event.key == pygame.K_RIGHT and player_pos < 2:
                player_pos += 1

    # Player position
    player_x = LANE_WIDTH * player_pos + LANE_WIDTH // 2 - player_size // 2
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    # Spawn obstacles and coins
    spawn_timer += 1
    if spawn_timer >= 30:  # Spawn every half-second
        spawn_obstacle()
        if random.random() < 0.5:  # 50% chance to spawn a coin
            spawn_coin()
        spawn_timer = 0

    # Update and draw obstacles
    for obstacle in obstacles[:]:
        obstacle["y"] += obstacle["speed"]
        # Pseudo-3D scaling effect based on y position
        size = int(obstacle["size"] * (1 + (obstacle["y"] / HEIGHT)))
        pygame.draw.rect(screen, RED, (obstacle["x"] - size // 2, obstacle["y"], size, size))

        # Check for collision with player
        if abs(obstacle["x"] - player_x) < player_size // 2 and player_y < obstacle["y"] < player_y + player_size:
            print("Game Over! Final Score:", score)
            running = False
            root.destroy()
        if obstacle["y"] > HEIGHT:
            obstacles.remove(obstacle)

    # Update and draw coins
    for coin in coins[:]:
        coin["y"] += coin["speed"]
        # Pseudo-3D scaling effect based on y position
        size = int(coin["size"] * (1 + (coin["y"] / HEIGHT)))
        pygame.draw.circle(screen, YELLOW, (coin["x"], coin["y"]), size // 2)

        # Check for collection
        if abs(coin["x"] - player_x) < player_size // 2 and player_y < coin["y"] < player_y + player_size:
            score += 1
            coins.remove(coin)
            score_label.config(text=f"Score: {score}")
        if coin["y"] > HEIGHT:
            coins.remove(coin)

    # Update Tkinter score display
    root.update_idletasks()
    root.update()

    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
