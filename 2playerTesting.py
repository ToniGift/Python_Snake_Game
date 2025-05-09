import tkinter as tk
import random
import sys

# Game parameters
win_x, win_y = 800, 800
snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]

# Initialize game window
snake_window = tk.Tk()
snake_window.geometry(f"{win_x}x{win_y}")
snake_window.resizable(0, 0)
snake_window.title("Snake")
snake_window.protocol("WM_DELETE_WINDOW", sys.exit)

# Game canvas
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()

# Snake parameters for Player 1
snake1_coords = [game_dimensions[0] // 4, game_dimensions[1] // 2]
snake1_tail = []
snake1_move_dir = [1, 0]
snake1_moved_in_this_frame = False

# Snake parameters for Player 2
snake2_coords = [game_dimensions[0] * 3 // 4, game_dimensions[1] // 2]
snake2_tail = []
snake2_move_dir = [-1, 0]
snake2_moved_in_this_frame = False

# Score and game state
score = [0, 0]
game_running = True

# Function to create grid items (snake segments, apples)
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

# Function for game loop
def gameloop():
    global snake1_moved_in_this_frame, snake2_moved_in_this_frame, snake1_coords, snake2_coords, snake1_tail, snake2_tail, score, apple_coords, game_running

    if not game_running:
        return

    snake_window.after(100, gameloop)
    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="#222222")

    # Player 1 movement
    snake1_tail.append(list(snake1_coords))
    snake1_coords[0] += snake1_move_dir[0]
    snake1_coords[1] += snake1_move_dir[1]

    # Player 2 movement
    snake2_tail.append(list(snake2_coords))
    snake2_coords[0] += snake2_move_dir[0]
    snake2_coords[1] += snake2_move_dir[1]

    # Collision detection
    if checkCollision(snake1_coords, snake1_tail) or checkCollision(snake2_coords, snake2_tail):
        game_over()

    # Display the snakes
    for segment in snake1_tail:
        createGridItem(segment, "#00ff00")
    for segment in snake2_tail:
        createGridItem(segment, "#0000ff")

    # Display an apple
    if apple_coords == snake1_coords:
        score[0] += 1
        apple_coords = generateAppleCoords()
    elif apple_coords == snake2_coords:
        score[1] += 1
        apple_coords = generateAppleCoords()
    else:
        snake1_tail.pop(0)
        snake2_tail.pop(0)

    createGridItem(apple_coords, "#ff0000")
    display_score()

# Function to check collisions
def checkCollision(coords, tail):
    if coords[0] < 0 or coords[0] >= game_dimensions[0] or coords[1] < 0 or coords[1] >= game_dimensions[1]:
        return True
    if coords in tail[:-1]:  # Exclude the head
        return True
    return False

# Function to handle keyboard input
def key(event):
    global snake1_move_dir, snake2_move_dir, snake1_moved_in_this_frame, snake2_moved_in_this_frame

    if not game_running:
        return

    if not snake1_moved_in_this_frame:
        snake1_moved_in_this_frame = True
        if event.keysym == "a" and snake1_move_dir[0] != 1:
            snake1_move_dir = [-1, 0]
        elif event.keysym == "d" and snake1_move_dir[0] != -1:
            snake1_move_dir = [1, 0]
        elif event.keysym == "w" and snake1_move_dir[1] != 1:
            snake1_move_dir = [0, -1]
        elif event.keysym == "s" and snake1_move_dir[1] != -1:
            snake1_move_dir = [0, 1]

    if not snake2_moved_in_this_frame:
        snake2_moved_in_this_frame = True
        if event.keysym == "Left" and snake2_move_dir[0] != 1:
            snake2_move_dir = [-1, 0]
        elif event.keysym == "Right" and snake2_move_dir[0] != -1:
            snake2_move_dir = [1, 0]
        elif event.keysym == "Up" and snake2_move_dir[1] != 1:
            snake2_move_dir = [0, -1]
        elif event.keysym == "Down" and snake2_move_dir[1] != -1:
            snake2_move_dir = [0, 1]

# Function to reset the game
def reset_game():
    global snake1_coords, snake2_coords, snake1_tail, snake2_tail, snake1_move_dir, snake2_move_dir, score, game_running, apple_coords
    snake1_coords = [game_dimensions[0] // 4, game_dimensions[1] // 2]
    snake2_coords = [game_dimensions[0] * 3 // 4, game_dimensions[1] // 2]
    snake1_tail.clear()
    snake2_tail.clear()
    snake1_move_dir = [1, 0]
    snake2_move_dir = [-1, 0]
    score = [0, 0]
    apple_coords = generateAppleCoords()
    game_running = True
    gameloop()

# Function to display score
def display_score():
    snake_canvas.create_text(50, 20, text=f"Score: Player 1 - {score[0]}, Player 2 - {score[1]}", fill="white", font=("Arial", 20))

# Function to display game over screen
def game_over():
    global game_running
    game_running = False

    game_over_window = tk.Toplevel(snake_window)
    game_over_window.title("Game Over")
    game_over_window.geometry("700x700")
    game_over_window.resizable(0, 0)

    # Load and display the Game Over image
    game_over_image = tk.PhotoImage(file="game.png")
    image_label = tk.Label(game_over_window, image=game_over_image)
    image_label.image = game_over_image
    image_label.pack(pady=10)

    tk.Label(game_over_window, text="Final Score: Player 1 - " + str(score[0]) + ", Player 2 - " + str(score[1]), font=("Arial", 16)).pack(pady=10)

    tk.Button(game_over_window, text="Play Again", command=lambda: [reset_game(), game_over_window.destroy()]).pack(pady=10)
    tk.Button(game_over_window, text="Quit", command=sys.exit).pack(pady=10)

# Initial apple placement
apple_coords = generateAppleCoords()

# Bind keyboard input
snake_window.bind("<KeyPress>", key)

# Start the game loop
gameloop()

# Run the game
snake_window.mainloop()
