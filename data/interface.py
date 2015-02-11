import sprites
import colour

__author__ = 'justin'
import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = pygame.Surface([width, height])
        #self.ob = ob
        #self.total = ob.get_health()
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        """Updates the location the healthbar based of the ob's location"""
        self.rect.x = x
        self.rect.y = y
        self.render()

    def update_bar(self, current, total):
        """Updates the health bar"""
        self.image.fill(colour.RED)
        self.image.fill(colour.B_GREEN, (0, 0, float(current)/total*self.width, self.height))

    def render(self):
        """Draws the health bar on screen"""
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class HealthBar2(HealthBar):
    """HealthBar Version 2. Updated to display health overlayed in percentage on the healthbar"""
    def __init__(self, x, y, width, height):
        HealthBar.__init__(self, x, y, width, height)
        self.font_ob = pygame.font.SysFont('arial', 15)

    def update_bar(self, current, total):
        """Updates the health bar"""
        self.image.fill(colour.RED)
        self.image.fill(colour.B_GREEN, (0, 0, float(current)/total*self.width, self.height))
        text = self.font_ob.render(str(float(current)/total*100) + "%", True, (0, 0, 0))
        pygame.draw.rect(self.image, colour.BLACK, (0, 0, self.width, self.height), 1)  #outline
        self.image.blit(text, ((self.width/2)-(text.get_width()/2), 0))

class AmmoBar(HealthBar):
    def update_bar(self, current, total):
        """Update ammunition bar"""
        self.image.fill(colour.WHITE)
        pygame.draw.rect(self.image, colour.J_GREEN, (0, 0, float(current)/total*self.width, self.height))
        pygame.draw.rect(self.image, colour.BLACK, (0, 0, self.width, self.height), 1)

    def render(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class Equip(object):
    def __init__(self, x, y):
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.defaults = {"bullet": sprites.bullet_icon(),
                         "rocket": sprites.rocketdrop(),
                         "dual": sprites.dual_bullet(),
                         "spread": sprites.spread_icon()}
        #self.set_weapon()

    def update(self, weapon):
        """Sets the equiped weapon ready to draw"""
        self.image = self.defaults[weapon]
        self.render()

    def render(self):
        """Redraws the current weapon box"""
        pygame.draw.rect(self.image, colour.BLACK, (0, 0, 20, 20), 1)
        self.screen.blit(self.image, (self.x, self.y))

class Text(object):
    """Basic text class"""
    def __init__(self, x, y, size, col):
        self.font_ob = pygame.font.SysFont('arial', size)
        #self.font_ob = pygame.font.Font('font/ka1.ttf', 20)
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.colour = col

    def render(self, text):
        """Redraws the text, call this to update"""
        text_sf = self.font_ob.render(text, True, self.colour)
        self.screen.blit(text_sf, (self.x, self.y))

class ArcadeText(Text):
    """Uses ka1.ttf font instead of system font"""
    def __init__(self, x, y, size, col):
        Text.__init__(self, x, y, size, col)
        self.font_ob = pygame.font.Font('font/ka1.ttf', size)

class Score(object):
    def __init__(self, x, y):
        self._score = 0
        self._text = ArcadeText(x, y, 20, colour.GREEN)
        self.update_score()

    def update_score(self, amount=0):
        self._score += amount
        self._text.render("Score: " + str(self._score))

    def render(self):
        self._text.render("Score: " + str(self._score))

class TextCenter(ArcadeText):
    """Inherits from ArcadeText, TextCenter automatically center aligns text"""
    def render(self, text):
        """Redraws the text in center pos, call this to update"""
        text_sf = self.font_ob.render(text, True, self.colour)
        self.screen.blit(text_sf, (self.x-text_sf.get_width()/2, self.y))


class TopStatusBar(object):
    """Class which represents the interface bar at the top of screen, it contains the score, health, ammo etc."""
    def __init__(self, health, ammo, equip, score):
        self.screen = pygame.display.get_surface()
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()
        self._health = health
        self._ammo = ammo
        self._equip = equip
        self._score = score

    def update(self):
        """Updates everything"""
        self._ammo.render()
        self._health.render()
        self._equip.render()
        self._score.render()

class ScrollText(object):
    """Basic text class to represent scrolling text"""
    def __init__(self, x, y, size, text, colour):
        self.font_ob = pygame.font.SysFont('arial', size)
        self.screen = pygame.display.get_surface()
        self.origin = (x, y)
        self._text_sf = self.font_ob.render(str(text), True, colour)
        self._x = x - self._text_sf.get_width()/2
        self._y = y

    def move_y(self, amount):
        """Moves the text by a given amount in the y-direction, and redraws the text"""
        self._y += amount
        self.screen.blit(self._text_sf, (self._x, self._y))

    def distance_travel(self):
        """Returns the difference in y coordinate from initialisation to present """
        return self.origin[1] - self._y

class SoundEffects(object):
    """class for controlling and maintaining sound effects"""
    def __init__(self):
        self.destroy = {"bullet": pygame.mixer.Sound("sounds/Laser_Shoot_Bullet.wav"),
                   "spread": pygame.mixer.Sound("sounds/Laser_Shoot_Spread.wav"),
                   "dual": pygame.mixer.Sound("sounds/Laser_Shoot.wav"),
                   "rocket": pygame.mixer.Sound("sounds/Explosion_Rocket.wav"),
                   "enemy": pygame.mixer.Sound("sounds/Explosion_Enemy.wav"),
                   "enemy_shoot": pygame.mixer.Sound("sounds/Laser_Shoot_Enemy.wav"),
                   "orb": pygame.mixer.Sound("sounds/Laser_Shoot_Eject.wav")
                    }
        self.powerup = {"weapon": pygame.mixer.Sound("sounds/Powerup_NewWeapon.wav"),
                        "health": pygame.mixer.Sound("sounds/Powerup_Health.wav"),
                        "speed": pygame.mixer.Sound("sounds/Powerup_Speed.wav"),
                        "ammo": pygame.mixer.Sound("sounds/Powerup_Ammo.wav"),
                        "shield": pygame.mixer.Sound("sounds/Powerup_Shield.wav")
                        }
        self.select = pygame.mixer.Sound("sounds/Blip_Select.wav")
        self.on = True

    def play_destroy(self, type, vol=0.7):
        if self.on:
            self.destroy[type].set_volume(vol)
            self.destroy[type].play()

    def play_powerup(self, type, vol=0.7):
        if self.on:
            self.powerup[type].set_volume(vol)
            self.powerup[type].play()

    def play_select(self):
        if self.on:
            self.select.play()

    def set_on(self, setting):
        self.on = setting



