import tkinter as tk
import random
import sys

# Game parameters
snake_window = tk.Tk()

# Game window size
win_x, win_y = 800, 800
snake_window.geometry(f"{win_x}x{win_y}")

# Block game window resize
snake_window.resizable(0, 0)
snake_window.title("Snake")
snake_window.protocol("WM_DELETE_WINDOW", sys.exit)

# Game canvas
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()

# Snake parameters
snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]
snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
snake_tail = []
snake_move_dir = [1, 0]
snake_moved_in_this_frame = False
wps = 10

# Score initialization
score = 0
game_running = True  # This will control whether the game is running or in game over state

# Functions
def createGridItem(coords, hexcolor):
    snake_canvas.create_rectangle(
        (coords[0]) * snake_scale, (coords[1]) * snake_scale,
        (coords[0] + 1) * snake_scale, (coords[1] + 1) * snake_scale, 
        fill=hexcolor, outline="#222222", width=3
    )

def generateAppleCoords():
    apple_coords = [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
    attempts = 0
    while apple_coords in snake_tail or apple_coords == snake_coords:
        if attempts > 100:  # Limit retries to avoid infinite loop
            return [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
        apple_coords = [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
        attempts += 1
    return apple_coords

def gameloop():
    global snake_tail, snake_coords, snake_move_dir, apple_coords, score, game_running, snake_moved_in_this_frame
    
    if not game_running:
        return

    snake_window.after(1000 // wps, gameloop)
    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="#222222")

    # Move the snake
    snake_coords[0] += snake_move_dir[0]
    snake_coords[1] += snake_move_dir[1]
    
    # Wall collision detection
    if (snake_coords[0] < 0 or snake_coords[0] >= game_dimensions[0] or
        snake_coords[1] < 0 or snake_coords[1] >= game_dimensions[1]):
        game_over()  # Trigger game over
        return

    # Add snake head to the tail
    snake_tail.append([snake_coords[0], snake_coords[1]])

    # Head-tail collision detection
    if snake_coords in snake_tail[:-1]:  # Exclude the head
        game_over()  # Trigger game over
        return

    # Display the snake
    for segment in snake_tail:
        createGridItem(segment, "#00ff00")

    # Display an apple
    createGridItem(apple_coords, "#ff0000")
    
    # Check if apple is eaten
    if apple_coords == snake_coords:
        apple_coords = generateAppleCoords()  # Generate new apple
        score += 1  # Increment score
    else:
        snake_tail.pop(0)  # Remove the tail if apple not eaten

    # Display the score
    display_score()
    snake_moved_in_this_frame = False  # Reset movement flag

def key(e):
    global snake_move_dir, snake_moved_in_this_frame
    
    if not game_running:
        return  # Do not allow movement if the game is over
    
    if not snake_moved_in_this_frame:
        snake_moved_in_this_frame = True
        
        if e.keysym == "Left" and snake_move_dir[0] != 1:
            snake_move_dir = [-1, 0]
        elif e.keysym == "Right" and snake_move_dir[0] != -1:
            snake_move_dir = [1, 0]
        elif e.keysym == "Up" and snake_move_dir[1] != 1:
            snake_move_dir = [0, -1]
        elif e.keysym == "Down" and snake_move_dir[1] != -1:
            snake_move_dir = [0, 1]

def reset_game():
    """Reset the game after a collision (wall or tail)."""
    global snake_coords, snake_tail, snake_move_dir, apple_coords, score, game_running
    snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]  # Reset snake position
    snake_tail = []  # Clear the tail
    snake_move_dir = [1, 0]  # Reset direction
    apple_coords = generateAppleCoords()  # Generate new apple
    score = 0  # Reset score
    game_running = True  # Set the game as running again
    gameloop()

def display_score():
    """Display the current score on the screen."""
    snake_canvas.create_text(50, 20, text=f"Score: {score}", fill="white", font=("Arial", 20))

def game_over():
    """Show the game over screen and provide an option to play again."""
    global game_running
    game_running = False  # Stop the game loop

    # Create a new top-level window for the Game Over screen
    game_over_window = tk.Toplevel(snake_window)
    game_over_window.title("Game Over")
    game_over_window.geometry("700x700")
    game_over_window.resizable(0, 0)

    # Load and display the Game Over image
    game_over_image = tk.PhotoImage(file="game.png")  # Load the image from the file
    image_label = tk.Label(game_over_window, image=game_over_image)
    image_label.image = game_over_image  # Keep a reference to the image to prevent garbage collection
    image_label.pack(pady=10)

    # Display final score
    tk.Label(game_over_window, text=f"Your Score: {score}", font=("Arial", 16)).pack(pady=10)

    # Play Again button
    tk.Button(game_over_window, text="Play Again", command=lambda: [reset_game(), game_over_window.destroy()]).pack(pady=10)

    # Quit button
    tk.Button(game_over_window, text="Quit", command=sys.exit).pack(pady=10)

# Place an apple
apple_coords = generateAppleCoords()

# Binding function
snake_window.bind("<KeyPress>", key)

# Start the game
gameloop()

# Display game window and check for keyboard event
snake_window.mainloop()

 