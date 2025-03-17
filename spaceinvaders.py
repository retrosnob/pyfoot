from _pyfoot import Actor, World, Game, PyFoot, Sound, Text
import os
import random

ASSETS_FOLDER = os.path.splitext(os.path.basename(__file__))[0]

# Load sounds
Sound.loadSound("shoot", os.path.join(ASSETS_FOLDER, "shoot.wav"))

# Define Player (Spaceship)
class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=50, height=20, color=(0, 255, 0))

    def act(self):
        if PyFoot.isKeyPressed("left") and self.x > 0:
            self.move(-5, 0)
        if PyFoot.isKeyPressed("right") and self.x + self.width < self.world.getWidth():
            self.move(5, 0)
        if PyFoot.wasKeyJustPressed("space"):
            self.world.addActor(Bullet(self.x + self.width // 2, self.y))
            Sound.playSound("shoot")

# Define Bullet
class Bullet(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=5, height=15, color=(255, 255, 0))

    def act(self):
        self.move(0, -5)
        if self.y < 0:
            self.world.removeActor(self)
        elif self.isTouching(Invader):
            invader = self.getOneIntersectingObject(Invader)
            self.world.removeActor(self)
            self.world.actors.remove(invader)
            Sound.playSound("explosion")
            self.world.updateScore()

# Define Invaders
class Invader(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=40, height=30, color=(255, 0, 0))

    def act(self):
        if random.random() < 0.001:
            self.world.addActor(EnemyBullet(self.x + self.width // 2, self.y + self.height))

# Define Enemy Bullet
class EnemyBullet(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=5, height=15, color=(255, 255, 255))

    def act(self):
        self.move(0, 5)
        if self.y > self.world.getHeight():
            self.world.removeActor(self)
        elif self.isTouching(Player):
            self.world.removeActor(self)
            Sound.playSound("explosion")
            self.world.gameOver()

# Create the world
class SpaceInvadersWorld(World):
    def __init__(self):
        super().__init__(width=800, height=600, bg_color=(0, 0, 0))
        self.score = 0
        self.score_display = Text(20, 20, "Score: 0", font_size=30, text_color=(255, 255, 255))
        self.addActor(self.score_display)
        self.addActor(Player(375, 550))
        for row in range(3):
            for col in range(8):
                self.addActor(Invader(100 + col * 60, 50 + row * 50))

    def updateScore(self):
        self.score += 10
        self.score_display.setText(f"Score: {self.score}")

    def gameOver(self):
        self.score_display.setText("GAME OVER")

# Start the game
world = SpaceInvadersWorld()
game = Game(world)
game.start()
