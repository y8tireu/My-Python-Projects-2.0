import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Fighting Game")

# Define Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Font settings for the menu
font = pygame.font.SysFont("comicsans", 50)


# Define Player Class
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.color = color
        self.velocity = 5
        self.health = 100

    def draw(self, ascreen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def attack(self, other_player):
        if self.x < other_player.x + other_player.width and \
                self.x + self.width > other_player.x and \
                self.y < other_player.y + other_player.height and \
                self.y + self.height > other_player.y:
            other_player.health -= 5


# Create Players
player1 = Player(100, 300, RED)
player2 = Player(600, 300, BLUE)


# Define AI behavior
def ai_movement(player, opponent):
    if player.x < opponent.x:
        player.x += player.velocity
    elif player.x > opponent.x:
        player.x -= player.velocity
    if player.y < opponent.y:
        player.y += player.velocity
    elif player.y > opponent.y:
        player.y -= player.velocity


# Draw button for the menu
def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))

    return False


# Main menu loop to select game mode
def game_menu():
    menu_running = True
    game_mode = None

    while menu_running:
        screen.fill(BLACK)

        title_text = font.render("Choose Game Mode", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        play_local = draw_button("Play Locally", 150, 300, 200, 80, RED, GREEN)
        play_ai = draw_button("Play Against AI", 450, 300, 200, 80, RED, GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if play_local:
            game_mode = "local"
            menu_running = False
        elif play_ai:
            game_mode = "ai"
            menu_running = False

        pygame.display.update()
        clock.tick(FPS)

    return game_mode


# Display winner and "New Game" button
def display_winner(winner_text):
    winner_running = True

    while winner_running:
        screen.fill(BLACK)
        winner_label = font.render(winner_text, True, WHITE)
        screen.blit(winner_label, (WIDTH // 2 - winner_label.get_width() // 2, HEIGHT // 3))

        new_game = draw_button("New Game", WIDTH // 2 - 100, HEIGHT // 2, 200, 80, RED, GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if new_game:
            winner_running = False
            main()  # Restart the game when "New Game" is clicked

        pygame.display.update()
        clock.tick(FPS)


# Main Game Loop
def main():
    game_mode = game_menu()  # Get game mode choice from menu

    if game_mode is None:
        return

    global player1, player2
    player1 = Player(100, 300, RED)
    player2 = Player(600, 300, BLUE)

    run_game = True
    two_player_mode = (game_mode == "local")

    while run_game:
        clock.tick(FPS)
        screen.fill(BLACK)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        # Player Movements (Local Play or Player vs AI)
        keys = pygame.key.get_pressed()

        # Player 1 Controls
        if keys[pygame.K_a] and player1.x - player1.velocity > 0:  # Left
            player1.x -= player1.velocity
        if keys[pygame.K_d] and player1.x + player1.width + player1.velocity < WIDTH:  # Right
            player1.x += player1.velocity
        if keys[pygame.K_w] and player1.y - player1.velocity > 0:  # Up
            player1.y -= player1.velocity
        if keys[pygame.K_s] and player1.y + player1.height + player1.velocity < HEIGHT:  # Down
            player1.y += player1.velocity
        if keys[pygame.K_SPACE]:  # Attack
            player1.attack(player2)

        # Player 2 Controls or AI
        if two_player_mode:
            if keys[pygame.K_LEFT] and player2.x - player2.velocity > 0:  # Left
                player2.x -= player2.velocity
            if keys[pygame.K_RIGHT] and player2.x + player2.width + player2.velocity < WIDTH:  # Right
                player2.x += player2.velocity
            if keys[pygame.K_UP] and player2.y - player2.velocity > 0:  # Up
                player2.y -= player2.velocity
            if keys[pygame.K_DOWN] and player2.y + player2.height + player2.velocity < HEIGHT:  # Down
                player2.y += player2.velocity
            if keys[pygame.K_RETURN]:  # Attack
                player2.attack(player1)
        else:
            ai_movement(player2, player1)
            if random.randint(0, 60) == 0:  # AI Random Attack
                player2.attack(player1)

        # Draw Players
        player1.draw(screen)
        player2.draw(screen)

        # Display Health
        pygame.draw.rect(screen, RED, (50, 50, player1.health * 2, 20))
        pygame.draw.rect(screen, BLUE, (WIDTH - 250, 50, player2.health * 2, 20))

        # Check for Winner
        if player1.health <= 0:
            winner_text = "Player 2 Wins!" if two_player_mode else "AI Wins!"
            display_winner(winner_text)
            run_game = False
        if player2.health <= 0:
            winner_text = "Player 1 Wins!"
            display_winner(winner_text)
            run_game = False

        # Update Display
        pygame.display.update()

    pygame.quit()


# Run the Game
if __name__ == "__main__":
    main()
