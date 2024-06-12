from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 5  # The distance the ball moves with each key press
BALL_RADIUS = 20
EATABLE_BALL_RADIUS = 4
BALL_COLOR = "#00FF00"
EATABLE_BALL_COLOR = ["#FFFF00","#FFC0CB","#A020F0", "#006bff" , "#ff0400"]
BACKGROUND_COLOR = "#000000"

class Ball():
    def __init__(self):
        self.ball_size = BALL_RADIUS
        self.current_coordinate = [350, 350]  # starting position
        self.ball_space = []

        self.ball = canvas.create_oval(
            self.current_coordinate[0] - self.ball_size,
            self.current_coordinate[1] - self.ball_size,
            self.current_coordinate[0] + self.ball_size,
            self.current_coordinate[1] + self.ball_size,
            fill=BALL_COLOR
        )

    def clear_ball(self):
        canvas.delete(self.ball)



class Eatable_Ball():

    def __init__(self):

        self.eatable_balls = []
        self.canvas_items = []  # List to keep track of canvas item IDs

        for i in range(200):
            coordinate = [random.randint(20,680) , random.randint(20,680)]
            self.eatable_balls.append(coordinate)

        for items in self.eatable_balls:
            item_id = canvas.create_oval(
                items[0] - EATABLE_BALL_RADIUS,
                items[1] - EATABLE_BALL_RADIUS,
                items[0] + EATABLE_BALL_RADIUS,
                items[1] + EATABLE_BALL_RADIUS,
                fill=random.choice(EATABLE_BALL_COLOR)
            )
            self.canvas_items.append(item_id)  # Store the created item ID

    def update_balls(self):
        for items in self.eatable_balls:
            item_id = canvas.create_oval(
                items[0] - EATABLE_BALL_RADIUS,
                items[1] - EATABLE_BALL_RADIUS,
                items[0] + EATABLE_BALL_RADIUS,
                items[1] + EATABLE_BALL_RADIUS,
                fill=random.choice(EATABLE_BALL_COLOR)
            )
            self.canvas_items.append(item_id)  # Store the created item ID

    def clear_balls(self):
        for item_id in self.canvas_items:
            canvas.delete(item_id)  # Delete the item from the canvas
        self.canvas_items.clear()  # Clear the list of item IDs

def move_ball():
    global score
    x, y = ball.current_coordinate

    if keys_pressed.get('Up') and keys_pressed.get('Left'):
        x -= SPACE_SIZE
        y -= SPACE_SIZE
    elif keys_pressed.get('Up') and keys_pressed.get('Right'):
        x += SPACE_SIZE
        y -= SPACE_SIZE
    elif keys_pressed.get('Down') and keys_pressed.get('Left'):
        x -= SPACE_SIZE
        y += SPACE_SIZE
    elif keys_pressed.get('Down') and keys_pressed.get('Right'):
        x += SPACE_SIZE
        y += SPACE_SIZE
    elif keys_pressed.get('Up'):
        y -= SPACE_SIZE
    elif keys_pressed.get('Down'):
        y += SPACE_SIZE
    elif keys_pressed.get('Left'):
        x -= SPACE_SIZE
    elif keys_pressed.get('Right'):
        x += SPACE_SIZE

    # Check for boundary conditions
    if x < BALL_RADIUS:
        x = BALL_RADIUS
    if x > GAME_WIDTH - BALL_RADIUS:
        x = GAME_WIDTH - BALL_RADIUS
    if y < BALL_RADIUS:
        y = BALL_RADIUS
    if y > GAME_HEIGHT - BALL_RADIUS:
        y = GAME_HEIGHT - BALL_RADIUS

    #updating the new positions
    ball.current_coordinate = [x, y]
    canvas.coords(ball.ball, x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS)



    for x in range(len(eatable_ball.eatable_balls)):
        if (abs(eatable_ball.eatable_balls[x][0] - ball.current_coordinate[0]) <= 10 and abs(eatable_ball.eatable_balls[x][1]  - ball.current_coordinate[1]) <= 10):
            score +=1
            canvas.delete(eatable_ball.canvas_items[x])
            eatable_ball.eatable_balls[x] = (1000,1000)
            #eatable_ball.update_balls()



def on_key_press(event):
    keys_pressed[event.keysym] = True
    move_ball()

def on_key_release(event):
    keys_pressed[event.keysym] = False

def countdown(time_left):
    global TimeForGame
    if time_left >= 0:
        label.config(text="Score: {} \t \t \t Time: {}".format(score, time_left))
        window.after(1000, countdown, time_left - 1)
    else:
        label.config(text="Score: {} \t \t Time is Over".format(score))

        ball.clear_ball()
        eatable_ball.eatable_balls.clear() # To handle Error in scoring
        eatable_ball.clear_balls()

        # You can add code here to handle the end of the game when the timer reaches 0

# Initialize the game window
window = Tk()
window.title("Ball Eater")
window.resizable(False, False)

score = 0
TimeForGame = 60

keys_pressed = {
    'Up': False,
    'Down': False,
    'Left': False,
    'Right': False
}

label = Label(window, text="Score: {} \t \t \t Time: {}".format(score, TimeForGame), font=('consolas', 20))
label.pack()  # Packs widgets relative to the earlier widget

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenmmwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_width / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind keyboard events to direction change
window.bind('<KeyPress>', on_key_press)
window.bind('<KeyRelease>', on_key_release)

# Start the countdown
countdown(TimeForGame)

# Create the ball
ball = Ball()
eatable_ball = Eatable_Ball()


window.mainloop()
