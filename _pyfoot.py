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

    def setRotation(self, angle):
        self.rotation = angle % 360

    def getRotation(self):
        return self.rotation

    def turn(self, degrees):
        self.rotation = (self.rotation + degrees) % 360

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
        self._to_remove = []

    def addActor(self, actor):
        actor.world = self
        self.actors.append(actor)
        if hasattr(actor, "addedToWorld"):  # Check if the method exists
            actor.addedToWorld()  # Call the method

    def removeActor(self, actor):
        if actor in self.actors:
            self._to_remove.append(actor)
            
    def update(self):
        for actor in self.actors:
            actor.act()
        for actor in self._to_remove:
            self.actors.remove(actor)
        self._to_remove.clear()            

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
    mouse_info = MouseInfo()
    _keys_pressed = set()
    _keys_held = set()
    _keys_released = set()

    @staticmethod
    def isKeyPressed(key_name):
        key = KEY_MAP.get(key_name)
        return key in PyFoot._keys_pressed if key else False

    @staticmethod
    def wasKeyJustPressed(key_name):
        key = KEY_MAP.get(key_name)
        if key and key in PyFoot._keys_pressed and key not in PyFoot._keys_held:
            PyFoot._keys_held.add(key)
            return True
        return False

    @staticmethod
    def _update_key_states():
        """Removes keys from _keys_held only if they were released."""
        for key in PyFoot._keys_released:
            PyFoot._keys_held.discard(key)
        PyFoot._keys_released.clear()

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
            PyFoot._update_key_states()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    PyFoot._keys_pressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    PyFoot._keys_pressed.discard(event.key)
                    PyFoot._keys_released.add(event.key)
                elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    PyFoot.mouse_info.update(event)
            
            self.world.update()
            self.world.draw(self.screen)
            self.clock.tick(self.fps)
        
        pygame.quit()
