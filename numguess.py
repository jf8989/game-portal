import random
import tkinter as tk
from tkinter import messagebox
import time
import json
import os
import winsound

# Load high scores from file
def load_high_scores():
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            return json.load(f)
    return {"Easy": 999, "Medium": 999, "Hard": 999}

# Save high scores to file
def save_high_scores(high_scores):
    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f)

# Function to run the number guessing game
def guess_number_game():
    high_scores = load_high_scores()
    min_value = 0
    max_value = 0
    secret_number = None
    attempts = 0
    start_time = 0
    theme_color = "#ffffff"

    def start_game():
        nonlocal min_value, max_value, secret_number, attempts, start_time
        try:
            difficulty = difficulty_var.get()
            if difficulty == "Easy":
                min_value, max_value = 1, 100
            elif difficulty == "Medium":
                min_value, max_value = 1, 500
            elif difficulty == "Hard":
                min_value, max_value = 1, 1000
            else:
                min_value = int(entry_min.get())
                max_value = int(entry_max.get())
            
            if min_value >= max_value:
                messagebox.showerror("Invalid Range", "Minimum value must be less than maximum value.")
                return

            secret_number = random.randint(min_value, max_value)
            print(f"[DEBUG] Secret number generated: {secret_number}")  # Debug log for the secret number
            attempts = 0
            start_time = time.time()
            range_frame.pack_forget()
            game_frame.pack(pady=20)
            result_label.config(text=f"I'm thinking of a number between {min_value:,} and {max_value:,}.", fg="black")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for the range.")

    def check_guess():
        nonlocal attempts, secret_number
        guess = entry_guess.get()
        print(f"[DEBUG] Current guess entry: {guess}")  # Debug log for the current entry value
        if not guess.isdigit():
            entry_guess.delete(0, tk.END)  # Clear the entry field immediately
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            print(f"[DEBUG] Invalid input received")  # Debug log for invalid input
            return
        
        guess = int(guess)
        print(f"[DEBUG] Player guessed: {guess}")  # Debug log for player's guess
        attempts += 1  # Increment the number of attempts by 1
        print(f"[DEBUG] Number of attempts: {attempts}")  # Debug log for number of attempts

        winsound.PlaySound("SystemHand", winsound.SND_ASYNC)  # Play sound for incorrect guess

        if guess < secret_number:
            print(f"[DEBUG] Guess {guess} is too low.")  # Debug log for too low guess
            result_label.config(text="Too low! Try again.", fg="red")
        elif guess > secret_number:
            print(f"[DEBUG] Guess {guess} is too high.")  # Debug log for too high guess
            result_label.config(text="Too high! Try again.", fg="red")
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)  # Play success sound
            print(f"[DEBUG] Guess {guess} is correct. Number of attempts: {attempts}")  # Debug log for correct guess
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            result_label.config(text=f"Congratulations! You guessed the number in {attempts} attempts and {elapsed_time} seconds.", fg="green")
            entry_guess.config(state='disabled')
            btn_check.config(state='disabled')
            btn_reset.pack(pady=10)

            # Update high scores
            difficulty = difficulty_var.get()
            if attempts < high_scores[difficulty]:
                high_scores[difficulty] = attempts
                save_high_scores(high_scores)
                messagebox.showinfo("New High Score!", f"New high score for {difficulty} level: {attempts} attempts!")
        entry_guess.delete(0, tk.END)  # Clear the entry field immediately
        # Rest of the operations below

    def reset_game():
        nonlocal secret_number, attempts, start_time
        attempts = 0
        secret_number = random.randint(min_value, max_value)
        print(f"[DEBUG] Secret number regenerated: {secret_number}")  # Debug log for new secret number
        entry_guess.config(state='normal')
        entry_guess.delete(0, tk.END)
        btn_check.config(state='normal')
        btn_reset.pack_forget()
        result_label.config(text=f"I'm thinking of a number between {min_value:,} and {max_value:,}.", fg="black")
        start_time = time.time()
        print(f"[DEBUG] Game has been reset with the same range.")  # Debug log for game reset

    def reset_interval():
        nonlocal min_value, max_value, secret_number, attempts
        game_frame.pack_forget()
        range_frame.pack(pady=20)
        entry_min.delete(0, tk.END)
        entry_max.delete(0, tk.END)
        secret_number = None
        attempts = 0
        print(f"[DEBUG] Interval has been reset.")  # Debug log for interval reset

    # Set up the GUI
    root = tk.Tk()
    print("[DEBUG] Initializing the GUI window")  # Debug log for GUI initialization
    root.title("Number Guessing Game")
    root.geometry("600x600")
    root.resizable(False, False)
    root.config(bg=theme_color)

    # Frame for selecting range
    range_frame = tk.Frame(root, bg=theme_color)
    tk.Label(range_frame, text="Select Difficulty or Enter Custom Range:", font=("Arial", 16), bg=theme_color, fg="#1e88e5").pack(pady=10)
    difficulty_var = tk.StringVar(value="Easy")
    tk.Radiobutton(range_frame, text="Easy (1-100)", variable=difficulty_var, value="Easy", font=("Arial", 12), bg=theme_color).pack()
    tk.Radiobutton(range_frame, text="Medium (1-500)", variable=difficulty_var, value="Medium", font=("Arial", 12), bg=theme_color).pack()
    tk.Radiobutton(range_frame, text="Hard (1-1000)", variable=difficulty_var, value="Hard", font=("Arial", 12), bg=theme_color).pack()
    tk.Label(range_frame, text="Or Enter Custom Range:", font=("Arial", 12), bg=theme_color, fg="#333333").pack()
    tk.Label(range_frame, text="Minimum Value:", font=("Arial", 12), bg=theme_color, fg="#333333").pack()
    entry_min = tk.Entry(range_frame, font=("Arial", 14), justify="center", relief="solid", bd=2)
    entry_min.pack(pady=5)
    tk.Label(range_frame, text="Maximum Value:", font=("Arial", 12), bg=theme_color, fg="#333333").pack()
    entry_max = tk.Entry(range_frame, font=("Arial", 14), justify="center", relief="solid", bd=2)
    entry_max.pack(pady=5)
    entry_max.bind('<Return>', lambda event: start_game())  # Bind Enter key to start_game function
    tk.Button(range_frame, text="Start Game", command=start_game, font=("Arial", 14), bg="#4CAF50", fg="white", activebackground="#388E3C", relief="raised", bd=3).pack(pady=20)
    range_frame.pack(pady=20)

    # Frame for the main game
    game_frame = tk.Frame(root, bg=theme_color)
    tk.Label(game_frame, text="Welcome to the Number Guessing Game!", font=("Arial", 22, "bold"), bg=theme_color, fg="#1e88e5").pack(pady=10)
    tk.Label(game_frame, text="Instructions:\n1. Guess the number between the selected range.\n2. Press ENTER to submit your guess.\n3. Press TAB to alternate between input fields.\n4. You can also click 'Check Guess' to submit.\n5. Press SPACE to restart the game once completed.\n6. Press 'X' to reset the interval.", font=("Arial", 12), bg=theme_color, fg="#333333", justify="left").pack(pady=10)
    result_label = tk.Label(game_frame, text="", font=("Arial", 16), bg=theme_color, fg="#333333")
    result_label.pack(pady=10)

    entry_guess = tk.Entry(game_frame, font=("Arial", 18), justify="center", relief="solid", bd=2)
    entry_guess.pack(pady=10, ipadx=10, ipady=5)
    entry_guess.bind('<Return>', lambda event: check_guess())  # Bind Enter key to check_guess function
    print("[DEBUG] Entry widget for player guess created")  # Debug log for entry widget creation

    btn_check = tk.Button(game_frame, text="Check Guess", command=check_guess, font=("Arial", 14), bg="#4CAF50", fg="white", activebackground="#388E3C", relief="raised", bd=3)
    btn_check.pack(pady=10)
    print("[DEBUG] Check Guess button created")  # Debug log for check button creation

    btn_reset = tk.Button(game_frame, text="Play Again", command=reset_game, font=("Arial", 14), bg="#0288d1", fg="white", activebackground="#0277bd", relief="raised", bd=3)
    btn_reset.pack_forget()

    btn_reset_interval = tk.Button(game_frame, text="Reset Interval", command=reset_interval, font=("Arial", 14), bg="#d32f2f", fg="white", activebackground="#c62828", relief="raised", bd=3)
    btn_reset_interval.pack(pady=10)
    root.bind('x', lambda event: reset_interval())  # Bind X key to reset_interval function
    root.bind('<space>', lambda event: reset_game())  # Bind Space key to reset_game function
    print("[DEBUG] Play Again button created but not packed yet")  # Debug log for reset button creation

    root.mainloop()
    print("[DEBUG] GUI event loop terminated")  # Debug log for GUI termination

# Entry point of the script
if __name__ == "__main__":
    print("[DEBUG] Starting the game")  # Debug log for starting the game
    guess_number_game()