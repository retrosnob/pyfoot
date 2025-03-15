from engine import Actor, World, Game, PyFoot, Sound, Text
# from engine2 import Actor, World, Game, PyFoot, Sound, Text
import random

# Define the Destroyer (Player)
class Destroyer(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=80, height=20, color=(0, 255, 0))

    def act(self):
        if PyFoot.is_key_pressed("left") and self.x > 0:
            self.move(-5, 0)
        if PyFoot.is_key_pressed("right") and self.x + self.width < self.world.getWidth():
            self.move(5, 0)
        if PyFoot.was_key_just_pressed("space"):
            self.world.add_actor(DepthCharge(self.x + self.width // 2, self.y + self.height))
            Sound.play_sound("drop")

# Define Submarine
class Submarine(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=60, height=15, color=(255, 0, 0))
        self.speed = random.choice([-2, -1, 1, 2])

    def act(self):
        self.move(self.speed, 0)
        if self.x < 0 or self.x + self.width > self.world.getWidth():
            self.speed = -self.speed

# Define Depth Charge
class DepthCharge(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=10, height=20, color=(255, 255, 0))

    def act(self):
        self.move(0, 5)
        if self.y > self.world.getHeight():
            self.world.actors.remove(self)
        elif self.isTouching(Submarine):
            sub = self.getOneIntersectingObject(Submarine)
            self.world.actors.remove(self)
            self.world.actors.remove(sub)
            Sound.play_sound("explosion")
            self.world.update_score()

# Create the world
class SubHuntWorld(World):
    def __init__(self):
        super().__init__(width=800, height=600, bg_color=(0, 0, 128))
        self.score = 0
        self.score_display = Text(20, 20, "Score: 0", font_size=30, text_color=(255, 255, 255))
        self.add_actor(self.score_display)
        self.add_actor(Destroyer(360, 50))
        for i in range(3):
            self.add_actor(Submarine(random.randint(100, 700), random.randint(200, 500)))

    def update_score(self):
        self.score += 10
        self.score_display.setText(f"Score: {self.score}")

# Load sounds
Sound.load_sound("drop", "drop.wav")
Sound.load_sound("explosion", "explosion.wav")

# Start the game
world = SubHuntWorld()
game = Game(world)
game.start()
