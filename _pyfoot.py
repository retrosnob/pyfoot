import pygame
import math

# Key mappings for easier input handling
KEY_MAP = {
    "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
    "space": pygame.K_SPACE, "escape": pygame.K_ESCAPE, "w": pygame.K_w, "s": pygame.K_s
}

class Actor:
    def __init__(self, x=0, y=0, width=50, height=50, color=(255, 0, 0)):
        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.color = color
        self.world = None
        self.rotation = 0

    def act(self):
        """Override this method in subclasses."""
        pass

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value  # Same for y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, angle):
        self._rotation = angle % 360

    def move(self, dx, dy=None):
        if dy is None:
            radians = math.radians(self.rotation)
            self.x += dx * math.cos(radians)
            self.y += dx * math.sin(radians)
        else:
            self.x += dx
            self.y += dy

    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def turn(self, degrees):
        self._rotation = (self._rotation + degrees) % 360

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def isTouching(self, cls):
        """Check if this actor is touching any actor of the given class."""
        for actor in self.world.actors:
            if isinstance(actor, cls) and self._intersects(actor):
                return True
        return False
    
    def getOneIntersectingObject(self, cls):
        """Return one actor of the given class that is touching this actor."""
        for actor in self.world.actors:
            if isinstance(actor, cls) and self._intersects(actor):
                return actor
        return None

    def _intersects(self, other):
        """Check if two actors' bounding boxes overlap."""
        return (
            self.x < other.x + other.width and
            self.x + self.width > other.x and
            self.y < other.y + other.height and
            self.y + self.height > other.y
        )    

class World:
    def __init__(self, width=800, height=600, bg_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.actors = []
        self._toRemove = []

    def addActor(self, actor):
        actor.world = self
        self.actors.append(actor)
        if hasattr(actor, "addedToWorld"):  # Check if the method exists
            actor.addedToWorld()  # Call the method

    def removeActor(self, actor):
        if actor in self.actors and actor not in self._toRemove:
            self._toRemove.append(actor)
            if hasattr(actor, "removedFromWorld"):  # Check if the method exists
                actor.removedFromWorld()
                            
    def update(self):
        for actor in self.actors:
            actor.act()
        for actor in self._toRemove:
            self.actors.remove(actor)
        self._toRemove.clear()            

    def draw(self, screen):
        screen.fill(self.bg_color)
        for actor in self.actors:
            actor.draw(screen)
        pygame.display.flip()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height        

class MouseInfo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.buttons = {1: False, 2: False, 3: False}

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.x, self.y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.x, self.y = event.pos
            self.buttons[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.buttons[event.button] = False

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def isButtonDown(self, button):
        return self.buttons.get(button, False)
    
class PyFoot:
    mouseInfo = MouseInfo()
    _keysPressed = set()
    _keysHeld = {}  # Now correctly tracks last pressed frame
    _keysReleased = set()
    _keyCooldowns = {}  # Stores cooldown times per key
    _frameCount = 0  # Global frame counter

    @staticmethod
    def setKeyCooldown(keyName, cooldownFrames):
        """Set a cooldown period for a key (in frames)."""
        key = KEY_MAP.get(keyName)
        if key:
            PyFoot._keyCooldowns[key] = cooldownFrames

    @staticmethod
    def isKeyPressed(key_name):
        key = KEY_MAP.get(key_name)
        if key and key in PyFoot._keysPressed:
            # Enforce cooldown
            last_pressed = PyFoot._keysHeld.get(key, -9999)
            cooldown = PyFoot._keyCooldowns.get(key, 0)
            if PyFoot._frameCount - last_pressed < cooldown:
                return False  # Still in cooldown period
            PyFoot._keysHeld[key] = PyFoot._frameCount  # Update last press time
            return True
        return False

    @staticmethod
    def _updateKeyStates():
        """Removes keys from _keys_held only if they were released."""
        for key in PyFoot._keysReleased:
            if key in PyFoot._keysHeld and PyFoot._frameCount - PyFoot._keysHeld[key] >= PyFoot._keyCooldowns.get(key, 0):
                del PyFoot._keysHeld[key]  # Ensure keys reset properly

        PyFoot._keysReleased.clear()
        PyFoot._frameCount += 1  # Advance frame count


class Text(Actor):
    def __init__(self, x, y, text, font_size=30, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        pygame.font.init()
        super().__init__(x, y)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = pygame.font.Font(None, font_size)

    def setText(self, new_text):
        self.text = new_text

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.text_color, self.bg_color)
        text_rect = text_surface.get_rect(topleft=(self.x, self.y))  # Aligns correctly
        screen.blit(text_surface, text_rect)

class Sound:
    pygame.mixer.init()
    sounds = {}

    @staticmethod
    def loadSound(name, filepath):
        """Load a sound from a file."""
        Sound.sounds[name] = pygame.mixer.Sound(filepath)

    @staticmethod
    def getSound(name):
        """Retrieve a sound safely, returning None if not found."""
        return Sound.sounds.get(name)

    @staticmethod
    def playSound(name, loop=False):
        """Play a loaded sound. If loop=True, play indefinitely."""
        sound = Sound.getSound(name)
        if sound:
            loops = -1 if loop else 0
            sound.play(loops=loops)

    @staticmethod
    def stopSound(name):
        """Stop a playing sound."""
        if name in Sound.sounds:
            Sound.sounds[name].stop()

    @staticmethod
    def setVolume(name, volume):
        """Set the volume of a loaded sound (0.0 to 1.0)."""
        if name in Sound.sounds:
            Sound.sounds[name].set_volume(volume)


class Game:
    def __init__(self, world, fps=30):
        pygame.init()
        pygame.font.init()
        self.world = world
        self.screen = pygame.display.set_mode((world.width, world.height))
        pygame.display.set_caption("PyFoot Game")
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = fps

    def start(self):
        self.running = True
        while self.running:
            PyFoot._updateKeyStates()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    PyFoot._keysPressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    PyFoot._keysPressed.discard(event.key)
                    PyFoot._keysReleased.add(event.key)
                elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    PyFoot.mouseInfo.update(event)
            
            self.world.update()
            self.world.draw(self.screen)
            self.clock.tick(self.fps)
        
        pygame.quit()
