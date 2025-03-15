from engine import Actor, World, Game, PyFoot, Text

# Define the paddles
class Paddle(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=10, height=100, color=(255, 255, 255))

    def act(self):
        if self.x < 400:  # Left paddle (Player 1)
            if PyFoot.is_key_pressed("up") and self.y > 0:
                self.move(0, -5)
            if PyFoot.is_key_pressed("down") and self.y + self.height < self.world.getHeight():
                self.move(0, 5)
        else:  # Right paddle (Player 2)
            if PyFoot.is_key_pressed("w") and self.y > 0:
                self.move(0, -5)
            if PyFoot.is_key_pressed("s") and self.y + self.height < self.world.getHeight():
                self.move(0, 5)

# Define the ball
class Ball(Actor):
    def __init__(self, x, y, left_score_display, right_score_display):
        super().__init__(x, y, width=15, height=15, color=(255, 255, 255))
        self.setRotation(45)  # Initial direction
        self.left_score_display = left_score_display
        self.right_score_display = right_score_display
        self.left_score = 0
        self.right_score = 0

    def act(self):
        self.move(5)  # Move in current direction

        # Bounce off top and bottom
        if self.y <= 0 or self.y + self.height >= self.world.getHeight():
            self.setRotation(-self.getRotation())  # Invert vertical direction

        # Bounce off paddles
        if self.isTouching(Paddle):
            self.setRotation(180 - self.getRotation())  # Reflect horizontally

        # Reset if ball goes out
        if self.x < 0:
            self.right_score += 1
            self.right_score_display.setText(f"{self.right_score}")
            self.reset_position()
        elif self.x > self.world.getWidth():
            self.left_score += 1
            self.left_score_display.setText(f"{self.left_score}")
            self.reset_position()

    def reset_position(self):
        self.setLocation(self.world.getWidth() // 2, self.world.getHeight() // 2)
        self.setRotation(45)  # Reset direction

# Create the world
world = World()

# Add paddles
left_paddle = Paddle(30, 250)
right_paddle = Paddle(760, 250)
world.add_actor(left_paddle)
world.add_actor(right_paddle)

# Add score displays
left_score_display = Text(300, 20, "0", font_size=40, text_color=(255, 255, 255), bg_color=(0, 0, 0))
right_score_display = Text(500, 20, "0", font_size=40, text_color=(255, 255, 255), bg_color=(0, 0, 0))
world.add_actor(left_score_display)
world.add_actor(right_score_display)

# Add ball
ball = Ball(400, 300, left_score_display, right_score_display)
world.add_actor(ball)

# Start the game
game = Game(world)
game.start()
