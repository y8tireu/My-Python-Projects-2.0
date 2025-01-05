import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = 800, 600
WHITE, BLACK, RED, BLUE, GREEN, YELLOW, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (128, 128, 128)
FULLSCREEN = False  # Initial fullscreen state

# Set up display
screen = pygame.display.set_mode((ORIGINAL_WIDTH, ORIGINAL_HEIGHT))
pygame.display.set_caption("Horror Game - Escape Granny")

# Game Variables
player_pos = [50, 50]
granny_pos = [random.randint(100, ORIGINAL_WIDTH-100), random.randint(100, ORIGINAL_HEIGHT-100)]
keys_collected = 0
inventory = []
rooms = 5  # Number of rooms to explore
game_active = False
admin_menu_active = False
invincible = False  # Admin option
admin_input = ""  # Text input for admin commands
granny_chasing = False
message_log = []  # List to hold console messages

# Screen dimensions (will update with full-screen toggle)
SCREEN_WIDTH, SCREEN_HEIGHT = ORIGINAL_WIDTH, ORIGINAL_HEIGHT
scaling_factor_x, scaling_factor_y = 1, 1  # Scaling factors to adjust positions and sizes

# Difficulty Settings
difficulty = None  # None until selected
granny_speed = 0.5
granny_chase_speed = 1.5
granny_detection_distance = 150

# Define game entities
door_positions = [[random.randint(100, ORIGINAL_WIDTH - 50), random.randint(100, ORIGINAL_HEIGHT - 50)] for _ in range(rooms)]
key_positions = [[random.randint(100, ORIGINAL_WIDTH - 50), random.randint(100, ORIGINAL_HEIGHT - 50)] for _ in range(rooms)]
weapon_position = [350, 250]
exit_position = [750, 550]

# Player attributes
player_speed = 3
running_speed = 5

# Player controls
player_controls = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'inventory': pygame.K_e,
    'run': pygame.K_LSHIFT,
    'shoot': pygame.K_RETURN
}

# Font for GUI
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Helper functions
def update_scaling_factors():
    """Update scaling factors based on current screen dimensions."""
    global scaling_factor_x, scaling_factor_y
    scaling_factor_x = SCREEN_WIDTH / ORIGINAL_WIDTH
    scaling_factor_y = SCREEN_HEIGHT / ORIGINAL_HEIGHT

def scale_position(pos):
    """Scale a position tuple according to the current scaling factors."""
    return [int(pos[0] * scaling_factor_x), int(pos[1] * scaling_factor_y)]

def draw_text_centered(text, y, color=WHITE):
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, ((SCREEN_WIDTH - text_surf.get_width()) // 2, y))

def add_message(message):
    """Add a message to the message log and limit it to the last 5 messages."""
    if len(message_log) >= 5:
        message_log.pop(0)
    message_log.append(message)

def draw_messages():
    """Draw the last few messages at the bottom of the screen."""
    y = SCREEN_HEIGHT - 100
    for message in message_log:
        message_surf = small_font.render(message, True, WHITE)
        screen.blit(message_surf, (10, y))
        y += 20

def draw_player():
    pygame.draw.rect(screen, BLUE, (*scale_position(player_pos), 30, 30))

def draw_granny():
    pygame.draw.circle(screen, GRAY, scale_position(granny_pos), 30)  # Granny's representation

def draw_items():
    for door in door_positions:
        pygame.draw.rect(screen, BLACK, (*scale_position(door), 50, 10))
    for key in key_positions:
        pygame.draw.circle(screen, YELLOW, scale_position(key), 5)
    pygame.draw.rect(screen, (128, 128, 128), (*scale_position(weapon_position), 10, 10))
    pygame.draw.rect(screen, GREEN, (*scale_position(exit_position), 60, 30))  # Car for escape

def move_player(keys):
    speed = running_speed if keys[player_controls['run']] else player_speed
    if keys[player_controls['left']]:
        player_pos[0] -= speed
    if keys[player_controls['right']]:
        player_pos[0] += speed
    if keys[player_controls['up']]:
        player_pos[1] -= speed
    if keys[player_controls['down']]:
        player_pos[1] += speed

def granny_behavior():
    global granny_chasing
    distance_to_player = abs(player_pos[0] - granny_pos[0]) + abs(player_pos[1] - granny_pos[1])

    # Granny chases player if within detection range
    if distance_to_player < granny_detection_distance:
        granny_chasing = True
    else:
        granny_chasing = False

    # Granny movement
    if granny_chasing:
        # Chase the player
        if player_pos[0] > granny_pos[0]:
            granny_pos[0] += granny_chase_speed
        else:
            granny_pos[0] -= granny_chase_speed
        if player_pos[1] > granny_pos[1]:
            granny_pos[1] += granny_chase_speed
        else:
            granny_pos[1] -= granny_chase_speed
    else:
        # Roam randomly
        direction = random.choice(['left', 'right', 'up', 'down'])
        if direction == 'left':
            granny_pos[0] -= granny_speed
        elif direction == 'right':
            granny_pos[0] += granny_speed
        elif direction == 'up':
            granny_pos[1] -= granny_speed
        elif direction == 'down':
            granny_pos[1] += granny_speed

def check_item_collision():
    global keys_collected
    for key in key_positions:
        if abs(player_pos[0] - key[0]) < 15 and abs(player_pos[1] - key[1]) < 15:
            keys_collected += 1
            key_positions.remove(key)
            add_message("Key collected!")
            break
    if abs(player_pos[0] - weapon_position[0]) < 15 and abs(player_pos[1] - weapon_position[1]) < 15:
        inventory.append("Weapon")
        add_message("Weapon collected!")
    if abs(player_pos[0] - exit_position[0]) < 15 and "Weapon" in inventory and keys_collected == len(door_positions):
        add_message("You escaped! Game Over")
        pygame.quit()
        exit()

def toggle_fullscreen():
    global FULLSCREEN, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        display_info = pygame.display.Info()
        SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        SCREEN_WIDTH, SCREEN_HEIGHT = ORIGINAL_WIDTH, ORIGINAL_HEIGHT
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    update_scaling_factors()
    add_message("Toggled fullscreen mode.")

def handle_admin_menu():
    global invincible, admin_input, key_positions, inventory
    command = admin_input.lower()
    if command == "godmode":
        invincible = True
        add_message("Godmode activated: You are now invincible!")
    elif command == "teleport":
        player_pos[0] = random.randint(0, SCREEN_WIDTH // scaling_factor_x - 30)
        player_pos[1] = random.randint(0, SCREEN_HEIGHT // scaling_factor_y - 30)
        add_message("Teleported player to a random location!")
    elif command == "spawn_key":
        key_positions.append(player_pos.copy())
        add_message("Spawned a key at the player's position!")
    elif command == "fullscreen":
        toggle_fullscreen()
    elif command == "/controls":
        add_message("Controls: Move: WASD, Run: Shift, Inventory: E, Shoot: Enter")
    elif command == "/show_inventory":
        add_message(f"Inventory: {inventory}")
    elif command == "/reset_keys":
        key_positions = [[random.randint(100, ORIGINAL_WIDTH - 50), random.randint(100, ORIGINAL_HEIGHT - 50)] for _ in range(rooms)]
        add_message("Keys have been reset to new random locations.")
    elif command == "/help":
        add_message("Commands: godmode, teleport, spawn_key, fullscreen, /controls, /show_inventory, /reset_keys, /help")
    admin_input = ""  # Clear input after processing

def display_admin_input():
    draw_text_centered(f"Admin Command: {admin_input}", SCREEN_HEIGHT // 2 - 100, WHITE)

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    keys = pygame.key.get_pressed()

    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for admin menu toggle (Ctrl + Shift + L)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l and keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT]:
                admin_menu_active = not admin_menu_active
                admin_input = ""  # Reset input when admin menu is opened

            elif admin_menu_active:
                # Handle text input in the admin menu
                if event.key == pygame.K_RETURN:
                    handle_admin_menu()  # Process command
                elif event.key == pygame.K_BACKSPACE:
                    admin_input = admin_input[:-1]  # Remove last character
                else:
                    admin_input += event.unicode  # Add character to command

    # Update player and granny movements
    move_player(keys)
    granny_behavior()
    check_item_collision()

    # Render the game
    screen.fill(BLACK)
    draw_player()
    draw_granny()
    draw_items()

    # Display messages and admin menu if active
    draw_messages()
    if admin_menu_active:
        display_admin_input()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
