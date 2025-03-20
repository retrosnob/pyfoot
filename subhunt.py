import os
import random
from _pyfoot import Actor, World, Game, PyFoot, Text, Sound

ASSETS_FOLDER = os.path.splitext(os.path.basename(__file__))[0]

# Load sounds
Sound.loadSound("drop_charge", os.path.join(ASSETS_FOLDER, "drop_charge.wav"))
Sound.loadSound("explosion", os.path.join(ASSETS_FOLDER, "explosion.wav"))

# Define Player (Ship)
class Ship(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=60, height=20, color=(0, 255, 0))
        PyFoot.setKeyCooldown("space", 30)  # Set a 10-frame cooldown for space key

    def act(self):
        if PyFoot.isKeyPressed("left") and self.x > 0:
            self.move(-5, 0)
        if PyFoot.isKeyPressed("right") and self.x + self.width < self.world.getWidth():
            self.move(5, 0)
        if PyFoot.isKeyPressed("space"):
            self.world.addActor(DepthCharge(self.x + self.width // 2, self.y + 10))
            Sound.playSound("drop_charge")

# Define Depth Charge
class DepthCharge(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=10, height=20, color=(255, 255, 0))

    def act(self):
        self.move(0, 5)
        if self.y > self.world.getHeight():
            self.world.removeActor(self)
        elif self.isTouching(Submarine):
            submarine = self.getOneIntersectingObject(Submarine)
            self.world.removeActor(self)
            self.world.removeActor(submarine)
            Sound.playSound("explosion")
            self.world.updateScore()

# Define Submarines
class Submarine(Actor):
    def __init__(self, x, y, speed):
        super().__init__(x, y, width=50, height=20, color=(255, 0, 0))
        self.speed = speed

    def act(self):
        self.move(self.speed, 0)
        if self.x < -self.width or self.x > self.world.getWidth():
            self.world.removeActor(self)

# Create the world
class SubHuntWorld(World):
    def __init__(self):
        super().__init__(width=800, height=600, bg_color=(0, 0, 50))
        self.score = 0
        self.score_display = Text(20, 20, "Score: 0", font_size=30, text_color=(255, 255, 255))
        self.addActor(self.score_display)
        self.addActor(Ship(375, 50))  # Ship at the top
        self.spawn_timer = 0

    def update(self):
        super().update() 
        self.spawn_timer += 1
        if self.spawn_timer > 50:
            self.spawn_timer = 0
            x = random.choice([-50, self.getWidth() + 50])
            speed = random.choice([-2, 2])
            self.addActor(Submarine(x, random.randint(100, 400), speed))

    def updateScore(self):
        self.score += 10
        self.score_display.setText(f"Score: {self.score}")

# Start the game
world = SubHuntWorld()
game = Game(world)
game.start()
