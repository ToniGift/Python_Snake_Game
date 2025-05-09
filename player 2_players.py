import tkinter as tk
import random
import sys

# Game parameters
win_x, win_y = 800, 800
snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]

# Snake coordinates and movement
snake_coords = [[game_dimensions[0] // 4, game_dimensions[1] // 2], [game_dimensions[0] * 3 // 4, game_dimensions[1] // 2]]
snake_tails = [[], []]
snake_move_dirs = [[1, 0], [-1, 0]]
apples_eaten = [0, 0]
apple_coords = [0, 0]
score = [0, 0]  
game_running = True

# Create the game window
snake_window = tk.Tk()
snake_window.geometry(f"{win_x}x{win_y}")
snake_window.resizable(0, 0)
snake_window.title("Snake Game")
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()

def createGridItem(coords, color):
    snake_canvas.create_rectangle(
        coords[0] * snake_scale, coords[1] * snake_scale,
        (coords[0] + 1) * snake_scale, (coords[1] + 1) * snake_scale,
        fill=color, outline="#222222", width=3
    )

def generateAppleCoords():
    while True:
        coords = [random.randint(0, game_dimensions[0] - 1), random.randint(0, game_dimensions[1] - 1)]
        if coords not in snake_tails[0] and coords not in snake_tails[1] and coords != snake_coords[0] and coords != snake_coords[1]:
            return coords

def checkCollision(coords, player):
    if (coords[0] < 0 or coords[0] >= game_dimensions[0] or coords[1] < 0 or coords[1] >= game_dimensions[1] or 
        coords in snake_tails[player] or coords == snake_coords[1 - player]):
        return True
    return False

def gameloop():
    global game_running, apple_coords
    if not game_running:
        return

    snake_canvas.delete("all")
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="#222222")

    for i in range(2):
        snake_tails[i].insert(0, list(snake_coords[i]))
        snake_coords[i][0] += snake_move_dirs[i][0]
        snake_coords[i][1] += snake_move_dirs[i][1]

        if checkCollision(snake_coords[i], i):
            game_over()

        if snake_coords[i] == apple_coords:
            apples_eaten[i] += 1
            score[i] += 1
            apple_coords = generateAppleCoords()
        else:
            snake_tails[i].pop()

        for segment in snake_tails[i]:
            createGridItem(segment, "#00ff00" if i == 0 else "#0000ff")
        createGridItem(snake_coords[i], "#00ff00" if i == 0 else "#0000ff")

    createGridItem(apple_coords, "#ff0000")
    display_score()

    # Check for winner based on apples eaten
    for i in range(2):
        if apples_eaten[i] >= 5:
            game_winner(i)

    snake_window.after(100, gameloop)

def display_score():
    snake_canvas.create_text(100, 20, text=f"Player A Score: {score[0]}", fill="white", font=("Arial", 20))
    snake_canvas.create_text(400, 20, text=f"Player B Score: {score[1]}", fill="white", font=("Arial", 20))

def key(event):
    directions = {"a": [-1, 0], "d": [1, 0], "w": [0, -1], "s": [0, 1],
                  "Left": [-1, 0], "Right": [1, 0], "Up": [0, -1], "Down": [0, 1]}
    if event.keysym in directions:
        player = 0 if event.keysym in "adws" else 1
        if snake_move_dirs[player] != [-directions[event.keysym][0], -directions[event.keysym][1]]:
            snake_move_dirs[player] = directions[event.keysym]

def reset_game():
    global snake_coords, snake_tails, snake_move_dirs, apples_eaten, apple_coords, score, game_running
    snake_coords = [[game_dimensions[0] // 4, game_dimensions[1] // 2], [game_dimensions[0] * 3 // 4, game_dimensions[1] // 2]]
    snake_tails = [[], []]
    snake_move_dirs = [[1, 0], [-1, 0]]
    apple_coords = generateAppleCoords()
    apples_eaten = [0, 0]
    score = [0, 0]
    game_running = True
    display_score()
    gameloop()

#def game_over():
 #  global game_running
  # game_running = False
   #show_game_over_window("Game Over", f"Final Score: Player A - {score[0]} | Player B - {score[1]}")
    
    
 

def game_winner(winner):
    global game_running
    game_running = False
    show_game_over_window("Game Over", f"Player {winner + 1} wins!")

def game_over():
    global game_running
    game_running = False
    show_game_over_window("Game Over", f"Final Score: Player A - {score[0]} | Player B - {score[1]}")

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
    tk.Label(game_over_window, text=f"Final Score: Player A - {score[0]} | Player B - {score[1]}", font=("Arial", 16)).pack(pady=10)

    # Play Again button
    tk.Button(game_over_window, text="Play Again", command=lambda: [reset_game(), game_over_window.destroy()]).pack(pady=10)

    # Quit button
    tk.Button(game_over_window, text="Quit", command=sys.exit).pack(pady=10)


# Start the game
apple_coords = generateAppleCoords()
snake_window.bind("<KeyPress>", key)
gameloop()
snake_window.mainloop()
