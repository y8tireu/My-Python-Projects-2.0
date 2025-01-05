import tkinter as tk
from tkinter import messagebox
import random

class Character:
    def __init__(self, name, color, health, speed, power):
        self.name = name
        self.color = color
        self.health = health
        self.speed = speed
        self.power = power

# Define some characters
characters = [
    Character("Ninja", "red", 100, 15, 10),
    Character("Samurai", "blue", 120, 10, 15),
    Character("Monk", "green", 80, 20, 8),
]

class Player:
    def __init__(self, canvas: tk.Canvas, x: int, y: int, character: Character):
        """
        Initializes the player with position and character attributes.
        """
        self.canvas = canvas
        self.character = character
        self.id = self.canvas.create_rectangle(x, y, x + 50, y + 60, fill=character.color)
        self.health = character.health
        self.energy = 0  # Energy for special moves
        self.special_move_ready = False
        self.speed = character.speed
        self.power = character.power
        self.is_blocking = False
        self.facing = 1 if x < 400 else -1  # Direction the player is facing

    def move(self, dx: int, dy: int) -> None:
        """
        Moves the player by dx and dy on the canvas.
        """
        self.canvas.move(self.id, dx * self.facing, dy)
        self.facing = 1 if dx > 0 else -1 if dx < 0 else self.facing

    def get_position(self) -> list:
        """
        Returns the current coordinates of the player.
        """
        return self.canvas.coords(self.id)

    def attack(self, opponent: "Player") -> None:
        """
        Performs an attack on the opponent.
        """
        if self._is_colliding(opponent):
            damage = self.power
            if opponent.is_blocking:
                damage = max(0, damage - 5)
            opponent.health -= damage
            self.energy = min(100, self.energy + 10)
            if self.energy == 100:
                self.special_move_ready = True
            # Visual feedback
            x, y, _, _ = opponent.get_position()
            self.canvas.create_text(x + 25, y - 10, text=f"-{damage}", fill="yellow", font=("Arial", 12))
            self.canvas.after(500, lambda: self.canvas.delete("damage"))

    def special_attack(self, opponent: "Player") -> None:
        """
        Performs a special attack on the opponent.
        """
        if self.special_move_ready and self._is_colliding(opponent):
            damage = self.power * 2
            opponent.health -= damage
            self.energy = 0
            self.special_move_ready = False
            # Visual feedback
            x, y, _, _ = opponent.get_position()
            self.canvas.create_text(x + 25, y - 30, text=f"Special! -{damage}", fill="orange", font=("Arial", 14))
            self.canvas.after(500, lambda: self.canvas.delete("damage"))

    def block(self, is_blocking: bool) -> None:
        """
        Sets the blocking state of the player.
        """
        self.is_blocking = is_blocking
        color = "grey" if is_blocking else self.character.color
        self.canvas.itemconfig(self.id, fill=color)

    def _is_colliding(self, opponent: "Player") -> bool:
        """
        Determines if the player is colliding with the opponent.
        """
        my_coords = self.get_position()
        opp_coords = opponent.get_position()
        return (my_coords and opp_coords and
                my_coords[0] < opp_coords[2] and my_coords[2] > opp_coords[0] and
                my_coords[1] < opp_coords[3] and my_coords[3] > opp_coords[1])

class FightingGame:
    MOVE_STEP = 10

    def __init__(self, root: tk.Tk):
        """
        Initializes the game window, players, controls, and the new game button.
        """
        self.root = root
        self.root.title("2 Player Fighting Game")

        # Game variables
        self.ai_mode = False
        self.difficulty = "Normal"

        # Create the main menu
        self.main_menu()

    def main_menu(self) -> None:
        """
        Sets up the main menu interface.
        """
        self.main_menu_frame = tk.Frame(self.root, bg="black")
        self.main_menu_frame.pack(fill="both", expand=True)

        title_label = tk.Label(self.main_menu_frame, text="2 Player Fighting Game",
                               font=("Arial", 30), bg="black", fg="white")
        title_label.pack(pady=50)

        start_button = tk.Button(self.main_menu_frame, text="Start Game", font=("Arial", 20),
                                 command=self.character_selection)
        start_button.pack(pady=10)

        ai_button = tk.Button(self.main_menu_frame, text="Play Against AI", font=("Arial", 20),
                              command=lambda: self.character_selection(ai_mode=True))
        ai_button.pack(pady=10)

        quit_button = tk.Button(self.main_menu_frame, text="Quit", font=("Arial", 20),
                                command=self.root.quit)
        quit_button.pack(pady=10)

    def character_selection(self, ai_mode=False) -> None:
        """
        Sets up the character selection screen.
        """
        self.ai_mode = ai_mode
        self.main_menu_frame.pack_forget()
        self.char_select_frame = tk.Frame(self.root, bg="black")
        self.char_select_frame.pack(fill="both", expand=True)

        tk.Label(self.char_select_frame, text="Player 1, choose your character:",
                 font=("Arial", 20), bg="black", fg="white").pack(pady=20)

        for idx, character in enumerate(characters):
            btn = tk.Button(self.char_select_frame, text=character.name, font=("Arial", 16),
                            command=lambda idx=idx: self.set_character(1, idx))
            btn.pack(pady=5)

    def set_character(self, player_num: int, char_idx: int) -> None:
        """
        Assigns the selected character to the player.
        """
        if player_num == 1:
            self.player1_char = characters[char_idx]
            if not self.ai_mode:
                self.char_select_frame.pack_forget()
                self.char_select_frame = tk.Frame(self.root, bg="black")
                self.char_select_frame.pack(fill="both", expand=True)
                tk.Label(self.char_select_frame, text="Player 2, choose your character:",
                         font=("Arial", 20), bg="black", fg="white").pack(pady=20)

                for idx, character in enumerate(characters):
                    btn = tk.Button(self.char_select_frame, text=character.name, font=("Arial", 16),
                                    command=lambda idx=idx: self.set_character(2, idx))
                    btn.pack(pady=5)
            else:
                self.player2_char = random.choice(characters)
                self.char_select_frame.pack_forget()
                self.difficulty_selection()
        else:
            self.player2_char = characters[char_idx]
            self.char_select_frame.pack_forget()
            self.start_game_screen()

    def difficulty_selection(self) -> None:
        """
        Allows the player to select the AI difficulty.
        """
        self.diff_select_frame = tk.Frame(self.root, bg="black")
        self.diff_select_frame.pack(fill="both", expand=True)

        tk.Label(self.diff_select_frame, text="Select AI Difficulty:",
                 font=("Arial", 20), bg="black", fg="white").pack(pady=20)

        difficulties = ["Easy", "Normal", "Hard"]
        for diff in difficulties:
            btn = tk.Button(self.diff_select_frame, text=diff, font=("Arial", 16),
                            command=lambda diff=diff: self.set_difficulty(diff))
            btn.pack(pady=5)

    def set_difficulty(self, difficulty: str) -> None:
        """
        Sets the AI difficulty.
        """
        self.difficulty = difficulty
        self.diff_select_frame.pack_forget()
        self.start_game_screen()

    def start_game_screen(self) -> None:
        """
        Configures the game screen and sets up players.
        """
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self.canvas.pack()

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack()

        # Initialize players
        self.player1 = Player(self.canvas, 100, 300, self.player1_char)
        self.player2 = Player(self.canvas, 600, 300, self.player2_char)

        self.setup_controls()
        self.game_loop()

    def setup_controls(self) -> None:
        """
        Configures key bindings for player movements and attacks.
        """
        self.root.bind("w", lambda event: self.player1.move(0, -self.player1.speed))
        self.root.bind("s", lambda event: self.player1.move(0, self.player1.speed))
        self.root.bind("a", lambda event: self.player1.move(-self.player1.speed, 0))
        self.root.bind("d", lambda event: self.player1.move(self.player1.speed, 0))
        self.root.bind("e", lambda event: self.player1.attack(self.player2))
        self.root.bind("r", lambda event: self.player1.special_attack(self.player2))
        self.root.bind("q", lambda event: self.player1.block(True))
        self.root.bind("<KeyRelease-q>", lambda event: self.player1.block(False))

        if not self.ai_mode:
            self.root.bind("<Up>", lambda event: self.player2.move(0, -self.player2.speed))
            self.root.bind("<Down>", lambda event: self.player2.move(0, self.player2.speed))
            self.root.bind("<Left>", lambda event: self.player2.move(-self.player2.speed, 0))
            self.root.bind("<Right>", lambda event: self.player2.move(self.player2.speed, 0))
            self.root.bind("/", lambda event: self.player2.attack(self.player1))
            self.root.bind(".", lambda event: self.player2.special_attack(self.player1))
            self.root.bind(",", lambda event: self.player2.block(True))
            self.root.bind("<KeyRelease-,>", lambda event: self.player2.block(False))

    def update_health_display(self) -> None:
        """
        Updates the health and energy display on the canvas.
        """
        self.canvas.delete("hud")
        # Player 1 HUD
        self.canvas.create_text(150, 50, text=f"{self.player1.character.name} Health: {self.player1.health}",
                                tag="hud", fill="red", font=("Arial", 14))
        self.canvas.create_rectangle(50, 70, 50 + self.player1.health * 2, 90, fill="red", tag="hud")
        self.canvas.create_text(150, 110, text=f"Energy: {self.player1.energy}%",
                                tag="hud", fill="yellow", font=("Arial", 14))
        # Player 2 HUD
        self.canvas.create_text(650, 50, text=f"{self.player2.character.name} Health: {self.player2.health}",
                                tag="hud", fill="blue", font=("Arial", 14))
        self.canvas.create_rectangle(550, 70, 550 + self.player2.health * 2, 90, fill="blue", tag="hud")
        self.canvas.create_text(650, 110, text=f"Energy: {self.player2.energy}%",
                                tag="hud", fill="yellow", font=("Arial", 14))

    def ai_behavior(self) -> None:
        """
        Controls the AI behavior for player 2.
        """
        # Difficulty settings
        if self.difficulty == "Easy":
            move_chance = 0.6
            attack_chance = 0.1
        elif self.difficulty == "Normal":
            move_chance = 0.8
            attack_chance = 0.3
        else:  # Hard
            move_chance = 1.0
            attack_chance = 0.5

        # AI Movement
        if random.random() < move_chance:
            p2_coords = self.player2.get_position()
            p1_coords = self.player1.get_position()
            dx = self.player2.speed if p2_coords[0] < p1_coords[0] else -self.player2.speed
            dy = self.player2.speed if p2_coords[1] < p1_coords[1] else -self.player2.speed
            self.player2.move(dx, dy)

        # AI Blocking
        if random.random() < 0.2:
            self.player2.block(True)
        else:
            self.player2.block(False)

        # AI Attack
        if random.random() < attack_chance:
            if self.player2.special_move_ready:
                self.player2.special_attack(self.player1)
            else:
                self.player2.attack(self.player1)

    def check_winner(self) -> bool:
        """
        Checks if any player has won and displays the result.
        """
        if self.player1.health <= 0:
            self.display_winner(f"{self.player2.character.name} Wins!", self.player2.character.color)
            return True
        if self.player2.health <= 0:
            self.display_winner(f"{self.player1.character.name} Wins!", self.player1.character.color)
            return True
        return False

    def display_winner(self, message: str, color: str) -> None:
        """
        Displays the winner message on the canvas.
        """
        self.canvas.create_text(400, 300, text=message, fill=color, font=("Arial", 36), tag="winner")
        self.root.after(2000, self.new_game)

    def game_loop(self) -> None:
        """
        Initiates the game loop.
        """
        if not self.check_winner():
            if self.ai_mode:
                self.ai_behavior()

            self.update_health_display()
            self.root.after(50, self.game_loop)

    def new_game(self) -> None:
        """
        Resets the game to its initial state and returns to the main menu.
        """
        # Hide the canvas and the "New Game" button
        self.canvas.pack_forget()
        self.new_game_button.pack_forget()

        # Clear the canvas of all elements
        self.canvas.delete("all")

        # Show the main menu again
        self.main_menu()

# Create the main window and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = FightingGame(root)
    root.mainloop()
#Explanation of Added Features
#1. Character Selection
#Introduced a Character class to define different fighters with unique attributes.
#Players can select from predefined characters like Ninja, Samurai, and Monk, each with different health, speed, and power.
#2. Special Attacks and Combos
#Added energy and special_move_ready attributes to the Player class.
#Players build up energy with each attack; when energy reaches 100%, they can perform a special attack.
#Special attacks deal more damage and have visual feedback.
#3. Health Bars and Energy Meters
#Implemented visual health bars and energy meters in the HUD (Heads-Up Display) using rectangles and text.
#4. Advanced AI Opponent
#Improved the AI behavior based on difficulty levels (Easy, Normal, Hard).
#AI now moves towards the player, decides when to block, and chooses between regular and special attacks.
#5. Multiplayer Options
#Retained local multiplayer support.
#Improved controls for both players, ensuring they don't conflict.
#6. Improved Graphics and Sound
#Added visual effects like damage indicators and special move notifications.
#(Note: Sound effects require additional libraries like pygame, which are not included here for simplicity.)
#7. Game Modes
#Simplified to focus on the main game mode.
#Added character and difficulty selection screens to enhance the game setup experience.
#How to Play the Enhanced Game
#Main Menu: Choose between "Start Game" for local multiplayer or "Play Against AI".
#Character Selection:
#Player 1: Select your character by clicking the buttons.
#Player 2: If playing against another player, they will also select a character. If playing against AI, the AI will randomly select a character.
#Difficulty Selection: If playing against AI, choose the difficulty level.
#Game Controls:
#Player 1:
#Move: W (up), A (left), S (down), D (right)
#Attack: E
#Special Attack: R
#Block: Hold Q
#Player 2:
#Move: Arrow Keys
#Attack: /
#Special Attack: .
#Block: Hold ,
#Objective: Reduce your opponent's health to zero using attacks and special moves while managing your energy and blocking incoming attacks.
#Additional Notes
#Energy Management: Attacking builds up your energy. Use special attacks wisely when your energy reaches 100%.
#Blocking: Reduces incoming damage. Time your blocks to minimize health loss.
#AI Behavior: The AI becomes more challenging on higher difficulties, reacting faster and using special attacks more effectively.