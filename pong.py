from _pyfoot import Actor, World, Game, PyFoot, Text, Sound
import os

ASSETS_FOLDER = os.path.splitext(os.path.basename(__file__))[0]

# Define Paddle
class Paddle(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=100, color=(255, 255, 255))

    def act(self):
        if self.x < 100:  # Left paddle
            if PyFoot.isKeyPressed("w") and self.y > 0:
                self.move(0, -5)
            if PyFoot.isKeyPressed("s") and self.y + self.height < self.world.getHeight():
                self.move(0, 5)
        else:  # Right paddle
            if PyFoot.isKeyPressed("up") and self.y > 0:
                self.move(0, -5)
            if PyFoot.isKeyPressed("down") and self.y + self.height < self.world.getHeight():
                self.move(0, 5)

# Define Ball
class Ball(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=15, height=15, color=(255, 255, 255))
        self.dx = 4
        self.dy = 4

    def act(self):
        self.move(self.dx, self.dy)
        if self.y <= 0 or self.y + self.height >= self.world.getHeight():
            self.dy = -self.dy  # Bounce off top and bottom
        if self.isTouching(Paddle):
            self.dx = -self.dx  # Reverse direction on paddle hit
        if self.x <= 0 or self.x + self.width >= self.world.getWidth():
            self.world.reset_ball()

# Define Pong World
class PongWorld(World):
    def __init__(self):
        super().__init__(width=800, height=600, bg_color=(0, 0, 0))
        self.score_left = 0
        self.score_right = 0
        self.score_display = Text(350, 20, "0 - 0", font_size=30, text_color=(255, 255, 255))
        self.addActor(self.score_display)
        self.left_paddle = Paddle(50, 250)
        self.right_paddle = Paddle(730, 250)
        self.ball = Ball(400, 300)
        self.addActor(self.left_paddle)
        self.addActor(self.right_paddle)
        self.addActor(self.ball)

    def reset_ball(self):
        if self.ball.x <= 0:
            self.score_right += 1
        else:
            self.score_left += 1
        self.score_display.setText(f"{self.score_left} - {self.score_right}")
        self.ball.setLocation(400, 300)
        self.ball.dx *= -1  # Change direction on reset

# Start the game
world = PongWorld()
game = Game(world)
game.start()
