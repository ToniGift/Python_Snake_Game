import tkinter as tk
import random
import sys

# Game parameters
win_x, win_y = 800, 800
snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]

# Snake coordinates and movement
snake1_coords = [game_dimensions[0] // 4, game_dimensions[1] // 2]
snake2_coords = [game_dimensions[0] * 3 // 4, game_dimensions[1] // 2]
snake1_tail = []
snake2_tail = []
snake1_move_dir = [1, 0]
snake2_move_dir = [-1, 0]
wps = 10  # Frames per second
apples_eaten = [0, 0]
apple_coords = [0, 0]
game_running = True
score = [0, 0]  # Variable to track the score for both players

# Function to create grid items
def createGridItem(coords, hexcolor):
    snake_canvas.create_rectangle(
        coords[0] * snake_scale, coords[1] * snake_scale,
        (coords[0] + 1) * snake_scale, (coords[1] + 1) * snake_scale,
        fill=hexcolor, outline="#222222", width=3
    )

# Function to generate apple coordinates
def generateAppleCoords():
    apple_coords = [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
    while apple_coords in snake1_tail or apple_coords in snake2_tail or apple_coords == snake1_coords or apple_coords == snake2_coords:
        apple_coords = [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
    return apple_coords

# Function to check collisions
def checkCollision(coords, tail, other_coords):
    if (coords[0] < 0 or coords[0] >= game_dimensions[0] or
        coords[1] < 0 or coords[1] >= game_dimensions[1]):
        return True  # Wall collision
    if coords in tail:
        return True  # Self-collision
    if coords == other_coords:
        return True  # Other snake head collision
    return False

# Game loop
def gameloop():
    global snake1_coords, snake2_coords, snake1_tail, snake2_tail, apple_coords, game_running

    if not game_running:
        return

    snake_window.after(1000 // wps, gameloop)
    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="#222222")

    # Move Snake 1
    snake1_tail.insert(0, list(snake1_coords))
    snake1_coords[0] += snake1_move_dir[0]
    snake1_coords[1] += snake1_move_dir[1]

    # Move Snake 2
    snake2_tail.insert(0, list(snake2_coords))
    snake2_coords[0] += snake2_move_dir[0]
    snake2_coords[1] += snake2_move_dir[1]

    # Check for collisions
    if (checkCollision(snake1_coords, snake1_tail, snake2_coords) or 
        checkCollision(snake2_coords, snake2_tail, snake1_coords)):
        game_over()

    # Display the snakes
    for segment in snake1_tail:
        createGridItem(segment, "#00ff00")
    for segment in snake2_tail:
        createGridItem(segment, "#0000ff")

    # Handle apple consumption and tail management
    if apple_coords == snake1_coords:
        apples_eaten[0] += 1
        score[0] += 1  # Increment score for Player 1
        apple_coords = generateAppleCoords()
    else:
        snake1_tail.pop()  # Remove the tail if apple not eaten

    if apple_coords == snake2_coords:
        apples_eaten[1] += 1
        score[1] += 1  # Increment score for Player 2
        apple_coords = generateAppleCoords()
    else:
        snake2_tail.pop()  # Remove the tail if apple not eaten

    createGridItem(apple_coords, "#ff0000")
    display_score()

# Display scores on the canvas
def display_score():
    """Display the current score on the screen."""
    snake_canvas.create_text(100, 20, text=f"Player 1 Score: {score[0]}", fill="white", font=("Arial", 20))
    snake_canvas.create_text(400, 20, text=f"Player 2 Score: {score[1]}", fill="white", font=("Arial", 20))

# Handle keyboard input
def key(event):
    global snake1_move_dir, snake2_move_dir

    if event.keysym == "a" and snake1_move_dir[0] != 1:
        snake1_move_dir = [-1, 0]
    elif event.keysym == "d" and snake1_move_dir[0] != -1:
        snake1_move_dir = [1, 0]
    elif event.keysym == "w" and snake1_move_dir[1] != 1:
        snake1_move_dir = [0, -1]
    elif event.keysym == "s" and snake1_move_dir[1] != -1:
        snake1_move_dir = [0, 1]

    if event.keysym == "Left" and snake2_move_dir[0] != 1:
        snake2_move_dir = [-1, 0]
    elif event.keysym == "Right" and snake2_move_dir[0] != -1:
        snake2_move_dir = [1, 0]
    elif event.keysym == "Up" and snake2_move_dir[1] != 1:
        snake2_move_dir = [0, -1]
    elif event.keysym == "Down" and snake2_move_dir[1] != -1:
        snake2_move_dir = [0, 1]

# Reset the game
def reset_game():
    global snake1_coords, snake2_coords, snake1_tail, snake2_tail, snake1_move_dir, snake2_move_dir, apple_coords, apples_eaten, game_running, score
    snake1_coords = [game_dimensions[0] // 4, game_dimensions[1] // 2]
    snake2_coords = [game_dimensions[0] * 3 // 4, game_dimensions[1] // 2]
    snake1_tail = []
    snake2_tail = []
    snake1_move_dir = [1, 0]
    snake2_move_dir = [-1, 0]
    apple_coords = generateAppleCoords()
    apples_eaten = [0, 0]
    score = [0, 0]  # Reset scores for both players
    game_running = True
    display_score()
    gameloop()

# Game over function
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

    # Display final scores
    tk.Label(game_over_window, text=f"Final Score: Player 1 - {score[0]} | Player 2 - {score[1]}", font=("Arial", 16)).pack(pady=10)

    # Play Again button
    tk.Button(game_over_window, text="Play Again", command=lambda: [reset_game(), game_over_window.destroy()]).pack(pady=10)

    # Quit button
    tk.Button(game_over_window, text="Quit", command=sys.exit).pack(pady=10)

# Initialize game window
snake_window = tk.Tk()
snake_window.geometry(f"{win_x}x{win_y}")
snake_window.resizable(0, 0)
snake_window.title("Snake Game")

# Initialize game canvas
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()

# Place an apple
apple_coords = generateAppleCoords()

# Bind keyboard input
snake_window.bind("<KeyPress>", key)

# Start the game loop
gameloop()

# Run the game
snake_window.mainloop()

