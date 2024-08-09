import tkinter as tk
import random
from tkinter import messagebox, filedialog

# Constants
GRID_LEVELS = {
    "Easy (3x3)": (3, 2),
    "Medium (4x4)": (4, 4),
    "Hard (10x10)": (10, 20)
}

# Create the Tkinter window
window = tk.Tk()
window.title("Minesweeper")

# Game variables
board = []
mines = set()
buttons = []
BOARD_SIZE = 0  # Default board size
NUM_MINES = 0  # Default number of mines
score = 0

# Function to update the game board in the GUI
def update_board_gui():
    for i in range(len(board)):
        for j in range(len(board[0])):
            button = buttons[i][j]
            if button['state'] == tk.NORMAL:
                button.config(text='')
            elif (i, j) in mines:
                button.config(text='', state=tk.DISABLED)
            else:
                button.config(state=tk.DISABLED)

# Function to handle button clicks
def button_click(row, col):
    global score
    score += 1
    # Check if the clicked button is a mine
    if (row, col) in mines:
        # Game over, show all mines
        for mine_row, mine_col in mines:
            button = buttons[mine_row][mine_col]
            button.config(text='*', state=tk.DISABLED)

        # Show game over message box
        messagebox.showinfo("Game Over", "You clicked on a mine! Game over.")
    else:
        # Count neighboring mines
        mine_count = 0
        for i in range(max(0, row-1), min(row+2, BOARD_SIZE)):
            for j in range(max(0, col-1), min(col+2, BOARD_SIZE)):
                if (i, j) in mines:
                    mine_count += 1

        # Update the button text with the mine count or mine symbol
        button = buttons[row][col]
        if mine_count > 0:
            button.config(text=str(mine_count))
        else:
            button.config(text='0')


# Function to save scores to a file
def save_scores():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "a") as file:
                file.write(str(score) + "\n")
            messagebox.showinfo("Score Saved", "Score saved successfully.")
            scores = []
            with open(file_path, "r") as file:
                scores = file.readlines()
            score_message = "Scores:\n" + "".join(scores)
            messagebox.showinfo("All Scores", score_message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving scores: {str(e)}")

# Function to start a new game with the selected grid level
def start_new_game():
    try:
        selected_level = level_dropdown.get()
        if selected_level in GRID_LEVELS:
            global board, mines, buttons, BOARD_SIZE, NUM_MINES, score
            board_size, num_mines = GRID_LEVELS[selected_level]
            BOARD_SIZE = board_size
            NUM_MINES = num_mines
            score = 0

            # Clear existing board and create new board
            for i in range(len(buttons)):
                for j in range(len(buttons[0])):
                    buttons[i][j].destroy()

            board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            mines = set()
            buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

            # Create buttons and assign commands
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    button = tk.Button(window, text='', width=2, height=1)
                    button.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=1)
                    button.config(command=lambda row=i, col=j: button_click(row, col))
                    buttons[i][j] = button

            # Place mines randomly on the board
            while len(mines) < NUM_MINES:
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - 1)
                mines.add((row, col))

            # Configure grid row and column to have equal weights
            for i in range(BOARD_SIZE):
                window.grid_columnconfigure(i, weight=1, uniform="group1")
                window.grid_rowconfigure(i+1, weight=1, uniform="group1")

            # Update the game board GUI
            update_board_gui()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while starting a new game: {str(e)}")

# Create the level dropdown bar
level_label = tk.Label(window, text="Select Level:")
level_label.grid(row=0, column=0, sticky="w")

level_dropdown = tk.StringVar(window)
level_dropdown.set("Easy (3x3)")
level_options = list(GRID_LEVELS.keys())

level_menu = tk.OptionMenu(window, level_dropdown, *level_options)
level_menu.grid(row=0, column=1, sticky="w")

start_button = tk.Button(window, text="Start New Game", command=start_new_game)
start_button.grid(row=0, column=2, sticky="w")

# Create the File menu
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Scores", command=save_scores)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
window.config(menu=menu_bar)

# Configure weights to make the button frame and level selection row expand
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Start the Tkinter event loop
window.mainloop()
