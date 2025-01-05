import openai
import os
import tkinter as tk
from tkinter import scrolledtext

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("")

def get_response(prompt):
    """Fetch response from OpenAI's API for the given prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use 'gpt-4' if available
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)  # Debugging print statement
        return error_message

def send_message(event=None):
    """Send the user's message to ChatGPT and display the response."""
    user_message = user_input.get()
    if user_message.strip() == "":
        return  # Ignore empty input

    # Display user message
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "You: " + user_message + "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

    # Get ChatGPT response
    response = get_response(user_message)

    # Display ChatGPT response
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "AI: " + response + "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

    # Clear input field
    user_input.delete(0, tk.END)

# Check if API key is set
if openai.api_key is None:
    print("Error: OpenAI API key is not set. Please set it as an environment variable named 'OPENAI_API_KEY'.")
else:
    # Set up the main application window
    app = tk.Tk()
    app.title("ChatGPT AI Chatbot")
    app.geometry("500x600")

    # Chat display area
    chat_display = scrolledtext.ScrolledText(app, wrap=tk.WORD, state=tk.DISABLED, width=60, height=25)
    chat_display.pack(padx=10, pady=10)

    # User input area
    user_input = tk.Entry(app, width=60)
    user_input.pack(padx=10, pady=10)
    user_input.bind("<Return>", send_message)  # Send message on Enter key press

    # Send button
    send_button = tk.Button(app, text="Send", command=send_message)
    send_button.pack(pady=5)

    # Run the app
    app.mainloop()
