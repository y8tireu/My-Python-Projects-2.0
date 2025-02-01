import customtkinter
import tkinter as tk  # Needed for some constants and widget methods

# Set the appearance and theme
customtkinter.set_appearance_mode("dark")  # Options: "dark", "light", "system"
customtkinter.set_default_color_theme("blue")  # You can choose other themes too

class GuessGame(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window with a larger size
        self.title("Guess Game")
        self.geometry("800x600")

        # Define a larger font for all widgets
        self.large_font = ("Helvetica", 20)

        # Create a centered frame to hold all the widgets with rounded corners
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Label prompting the user
        self.prompt_label = customtkinter.CTkLabel(
            self.main_frame,
            text="Enter a word or number:",
            font=self.large_font
        )
        self.prompt_label.pack(pady=(40, 20))

        # Entry widget for user input
        self.user_entry = customtkinter.CTkEntry(
            self.main_frame,
            placeholder_text="Your input here",
            font=self.large_font
        )
        # ipadx and ipady increase the inner padding of the entry widget
        self.user_entry.pack(pady=10, ipadx=10, ipady=10)

        # Submit button
        self.submit_button = customtkinter.CTkButton(
            self.main_frame,
            text="Submit",
            command=self.on_submit,
            font=self.large_font
        )
        self.submit_button.pack(pady=10)

        # Label to display the guess
        self.guess_label = customtkinter.CTkLabel(
            self.main_frame,
            text="",
            font=self.large_font
        )
        self.guess_label.pack(pady=20)

    def on_submit(self):
        """Handle the submit action."""
        user_input = self.user_entry.get()

        # Update the label to inform the user of the waiting period
        self.guess_label.configure(text="Guessing...")

        # Disable the input fields to prevent changes during the delay
        self.submit_button.configure(state="disabled")
        self.user_entry.configure(state="disabled")

        # Schedule display_guess to run after 2000 milliseconds (2 seconds)
        self.after(2000, lambda: self.display_guess(user_input))

    def display_guess(self, guess):
        """Display the guess after the delay."""
        self.guess_label.configure(text=f"My guess is: {guess}")

        # Re-enable the input fields for another round
        self.submit_button.configure(state="normal")
        self.user_entry.configure(state="normal")
        self.user_entry.delete(0, tk.END)  # Clear the entry

if __name__ == "__main__":
    app = GuessGame()
    app.mainloop()
