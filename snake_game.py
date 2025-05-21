import tkinter as tk
import random

# Constants
ROWS, COLS, TILE_SIZE = 25, 25, 25
WINDOW_WIDTH, WINDOW_HEIGHT = TILE_SIZE * COLS, TILE_SIZE * ROWS
FPS = 100  # in ms (100 = 10 FPS)

# Tile class
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Snake class
class Snake:
    def __init__(self, x, y):
        self.head = Tile(x, y)
        self.body = []
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        if self.velocity_x == 0 and self.velocity_y == 0:
            return

        # Move body
        if self.body:
            self.body = [Tile(self.head.x, self.head.y)] + self.body[:-1]

        # Move head
        self.head.x += self.velocity_x * TILE_SIZE
        self.head.y += self.velocity_y * TILE_SIZE

    def grow(self):
        self.body.append(Tile(self.head.x, self.head.y))

    def check_collision(self):
        return any(tile.x == self.head.x and tile.y == self.head.y for tile in self.body)

    def set_direction(self, dx, dy):
        # Prevent reversing
        if (dx == -self.velocity_x and dy == -self.velocity_y) or (dx == self.velocity_x and dy == self.velocity_y):
            return
        self.velocity_x, self.velocity_y = dx, dy

# Game class
class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("U-Beee Pro Snake")
        master.resizable(False, False)

        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{(master.winfo_screenwidth()//2)-(WINDOW_WIDTH//2)}+{(master.winfo_screenheight()//2)-(WINDOW_HEIGHT//2)}")

        # Initialize game
        self.snake = Snake(5 * TILE_SIZE, 5 * TILE_SIZE)
        self.food = self.random_food()
        self.score = 0
        self.game_over = False

        master.bind("<KeyPress>", self.change_direction)
        self.update()

    def random_food(self):
        return Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)

    def change_direction(self, e):
        if e.keysym == "Up":
            self.snake.set_direction(0, -1)
        elif e.keysym == "Down":
            self.snake.set_direction(0, 1)
        elif e.keysym == "Left":
            self.snake.set_direction(-1, 0)
        elif e.keysym == "Right":
            self.snake.set_direction(1, 0)
        elif e.keysym == "space" and self.game_over:
            self.restart()

    def update(self):
        if not self.game_over:
            self.snake.move()

            # Check collisions
            if (self.snake.head.x < 0 or self.snake.head.x >= WINDOW_WIDTH or
                self.snake.head.y < 0 or self.snake.head.y >= WINDOW_HEIGHT or
                self.snake.check_collision()):
                self.game_over = True

            # Food collision
            if self.snake.head.x == self.food.x and self.snake.head.y == self.food.y:
                self.snake.grow()
                self.food = self.random_food()
                self.score += 1

        self.render()
        self.master.after(FPS, self.update)

    def render(self):
        self.canvas.delete("all")

        # Draw food
        self.canvas.create_rectangle(self.food.x, self.food.y, self.food.x + TILE_SIZE, self.food.y + TILE_SIZE, fill="red")

        # Draw snake head
        self.canvas.create_rectangle(self.snake.head.x, self.snake.head.y, self.snake.head.x + TILE_SIZE, self.snake.head.y + TILE_SIZE, fill="lime")

        # Draw snake body
        for tile in self.snake.body:
            self.canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime")

        # Draw score and game over message
        self.canvas.create_text(50, 20, fill="white", font="Arial 12 bold", text=f"Score: {self.score}")

        if self.game_over:
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, fill="white", font="Arial 20 bold",
                                    text=f"GAME OVER\nScore: {self.score}\nPress SPACE to Restart")

    def restart(self):
        self.snake = Snake(5 * TILE_SIZE, 5 * TILE_SIZE)
        self.food = self.random_food()
        self.score = 0
        self.game_over = False

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()