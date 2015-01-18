__author__ = 'justin'
import pygame
import colour
import sprites

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, ob, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = pygame.Surface([width,height])
        self.ob = ob
        self.total = ob.get_health()
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        """Updates the location the healthbar based of the ob's location"""
        self.rect.x = self.ob.getx()
        self.rect.y = self.ob.gety() + self.ob.height + 2
        self.update_bar()

    def update_bar(self):
        """Redraws the health bar"""
        self.image.fill(colour.RED)
        if self.ob.get_health() <= 0:
            self.kill()
        else:
            self.image.fill(colour.B_GREEN, (0, 0, float(self.ob.get_health())/self.total*self.width, self.height))
            self.screen.blit(self.image, (self.rect.x,self.rect.y))

class HealthBar2(HealthBar):
    """HealthBar Version 2. Need to pass Ship object. Also displays health overlayed in percentage on the healthbar"""
    def __init__(self, ob, x, y, width, height):
        HealthBar.__init__(self, ob, x, y, width, height)
        self.font_ob = pygame.font.SysFont('arial', 15)

    def update_bar(self):
        """Redraws the health bar"""
        self.image.fill(colour.RED)
        self.image.fill(colour.B_GREEN, (0, 0, float(self.ob.get_health())/self.total*self.width, self.height))
        text = self.font_ob.render(str(float(self.ob.get_health())/self.total*100) + "%", True, (0, 0, 0))
        pygame.draw.rect(self.image, colour.BLACK, (0, 0, self.width, self.height), 1)

        self.image.blit(text, ((self.width/2)-(text.get_width()/2), 0))
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class AmmoBar(HealthBar):
    def update_bar(self):
        """Redraws ammunition bar"""
        self.image.fill(colour.WHITE)
        pygame.draw.rect(self.image, colour.J_GREEN, (0, 0, float(self.ob.get_ammo())/self.ob.get_ammolimit()*self.width, self.height))
        pygame.draw.rect(self.image, colour.BLACK, (0, 0, self.width, self.height), 1)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class Equip(object):
    def __init__(self, ship, x, y):
        self.screen = pygame.display.get_surface()
        self.ship = ship
        self.x = x
        self.y = y
        self.defaults = {"bullet": sprites.bullet_icon(),
                         "rocket": sprites.rocketdrop(),
                         "dual": sprites.dual_bullet(),
                         "default": sprites.startweponicon()}
        self.set_weapon()

    def set_weapon(self):
        """Sets the equiped weapon ready to draw"""
        self.image = self.defaults[self.ship.get_weapon()]
        self.update()

    def update(self):
        """Redraws the current weapon box"""
        pygame.draw.rect(self.image, colour.BLACK, (0, 0, 20, 20), 1)
        self.screen.blit(self.image, (self.x, self.y))

class Text(object):
    """Basic text class"""
    def __init__(self, x, y, size):
        self.font_ob = pygame.font.SysFont('arial', size)
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y

    def render(self, text):
        """Redraws the text, call this to update"""
        text_sf = self.font_ob.render(text, True, colour.WHITE)
        self.screen.blit(text_sf, (self.x, self.y))

class TextCenter(Text):
    """Inherits for Text, TextCenter automatically center aligns text"""
    def render(self, text):
        """Redraws the text in center pos, call this to update"""
        text_sf = self.font_ob.render(text, True, colour.WHITE)
        self.screen.blit(text_sf, (self.x-text_sf.get_width()/2, self.y))


class TopStatusBar(object):
    """Class which represents the interface bar at the top of screen, it contains the score, health, ammo etc."""
    def __init__(self, ship):
        self.screen = pygame.display.get_surface()
        self.screen_w = self.screen.get_rect()[2]
        self.screen_h = self.screen.get_rect()[3]
        self.ship = ship
        self.health = HealthBar2(self.ship, self.screen_w*0.75, self.screen_h*0.02, 175, 18)
        self.ammo = AmmoBar(self.ship, self.screen_w*0.50, self.screen_h*0.02, 175, 18)
        self.equip = Equip(self.ship, self.screen_w*0.30, self.screen_h*0.02)
        self.score = Text(self.screen_w*0.07, self.screen_h*0.02, 20)

    def new_equip(self):
        """Just updates the equip box"""
        self.equip.set_weapon()

    def update(self):
        """Updates everything"""
        self.ammo.update_bar()
        self.health.update_bar()
        self.equip.update()
        self.score.render('SCORE: ' + str(self.ship.get_score()))

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


class BotStatusBar(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_w = self.screen.get_rect()[2]
        self.screen_h = self.screen.get_rect()[3]
        self.message = None
        self.text = Text(self.screen_w*0.04, self.screen_h*0.95 , 18)

    def display(self, text):
        self.message = text
        self.update()

    def update(self):
        self.text.render(self.message)