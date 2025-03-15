from _pyfoot import Actor, World, Game, PyFoot, Sound, Text
import os
import random

ASSETS_FOLDER = os.path.splitext(os.path.basename(__file__))[0]

# Define Player (Spaceship)
class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=50, height=20, color=(0, 255, 0))

    def act(self):
        if PyFoot.is_key_pressed("left") and self.x > 0:
            self.move(-5, 0)
        if PyFoot.is_key_pressed("right") and self.x + self.width < self.world.getWidth():
            self.move(5, 0)
        if PyFoot.was_key_just_pressed("space"):
            self.world.add_actor(Bullet(self.x + self.width // 2, self.y))
            Sound.play_sound("shoot")

# Define Bullet
class Bullet(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=5, height=15, color=(255, 255, 0))

    def act(self):
        self.move(0, -5)
        if self.y < 0:
            self.world.remove_actor(self)
        elif self.isTouching(Invader):
            invader = self.getOneIntersectingObject(Invader)
            self.world.remove_actor(self)
            self.world.actors.remove(invader)
            Sound.play_sound("explosion")
            self.world.update_score()

# Define Invaders
class Invader(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=40, height=30, color=(255, 0, 0))

    def act(self):
        if random.random() < 0.001:
            self.world.add_actor(EnemyBullet(self.x + self.width // 2, self.y + self.height))

# Define Enemy Bullet
class EnemyBullet(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, width=5, height=15, color=(255, 255, 255))

    def act(self):
        self.move(0, 5)
        if self.y > self.world.getHeight():
            self.world.remove_actor(self)
        elif self.isTouching(Player):
            self.world.remove_actor(self)
            Sound.play_sound("explosion")
            self.world.game_over()

# Create the world
class SpaceInvadersWorld(World):
    def __init__(self):
        super().__init__(width=800, height=600, bg_color=(0, 0, 0))
        self.score = 0
        self.score_display = Text(20, 20, "Score: 0", font_size=30, text_color=(255, 255, 255))
        self.add_actor(self.score_display)
        self.add_actor(Player(375, 550))
        for row in range(3):
            for col in range(8):
                self.add_actor(Invader(100 + col * 60, 50 + row * 50))

    def update_score(self):
        self.score += 10
        self.score_display.setText(f"Score: {self.score}")

    def game_over(self):
        self.score_display.setText("GAME OVER")

# Load sounds
Sound.load_sound("shoot", "shoot.wav")
Sound.load_sound("explosion", "explosion.wav")

# Start the game
world = SpaceInvadersWorld()
game = Game(world)
game.start()
