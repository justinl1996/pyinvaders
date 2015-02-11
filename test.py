from data import colour
from data import interface

__author__ = 'justin'
import pygame

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class ScrollText(object):
    """Basic text class to represent scrolling text"""
    def __init__(self, x, y, size, text, colour):
        self.font_ob = pygame.font.SysFont('arial', size)
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.text_sf = self.font_ob.render(text, True, colour)

    def move_y(self, amount):
        """Moves the text by a given amount in the y-direction, and redraws the text"""
        self.y += amount
        self.screen.blit(self.text_sf, (self.x, self.y))

def speedboost():
    image = pygame.Surface([20, 20])
    image.fill(colour.SILVER)
    pygame.draw.polygon(image, colour.YELLOW, [(0, 15), (10, 4), (20, 15)])
    pygame.draw.polygon(image, colour.SILVER, [(0, 19), (10, 9), (20, 19)])
    return image

def spread_icon():
    """Draws the icon representing the spread weapon (3x dot bullet)"""
    text = pygame.font.SysFont('arial', 10).render("x3", True, (0, 0, 0))
    image = pygame.Surface([20, 20])
    image.fill(colour.SILVER)
    image.blit(text, (10, 8))
    pygame.draw.circle(image, colour.BLUE, (6, 10), 4, 0)
    return image


def invader():
    image = pygame.Surface([30, 25], pygame.SRCALPHA)
    pygame.draw.rect(image, colour.GREEN, (5, 0, 20, 20))
    pygame.draw.rect(image, colour.BLACK, (7, 5, 4, 4))
    pygame.draw.rect(image, colour.BLACK, (19, 5, 4, 4))
    pygame.draw.rect(image, colour.BLACK, (10, 13, 10, 4))
    pygame.draw.rect(image, colour.GREEN, (0, 15, 5, 15))
    pygame.draw.rect(image, colour.GREEN, (25, 15, 5, 10))
    pygame.image.save(image, "invader.tga")
    return image

def orb():
    image = pygame.Surface([16, 16], pygame.SRCALPHA)
    pygame.draw.circle(image, colour.BLACK, (8, 8), 8, 0)
    return image

def shield_drop():
    image = pygame.Surface([10, 10], pygame.SRCALPHA)
    pygame.draw.circle(image, colour.BLUE, (5, 5), 5, 0)
    pygame.draw.circle(image, colour.WHITE, (5, 5), 3, 0)
    return image


text = pygame.font.SysFont('arial', 20)

def instructions():
    image = pygame.Surface([200, 300], pygame.SRCALPHA)

    image.render(" arrow")

clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    #screen.fill((255, 255, 255))
    screen.fill((0, 0, 0))
    #screen.blit(speedboost(), (WIDTH/2, HEIGHT/2))
    #screen.blit(invader(), (WIDTH/2, HEIGHT/2))
    #screen.blit(spread_icon(), (WIDTH/2, HEIGHT/2))
    #screen.blit(orb_img, (300 + 30*math.cos(time), 300 + 30*math.sin(time)))
    #screen.blit(orb_img, (300 + 30*math.cos(time+2*math.pi/3), 300 + 30*math.sin(time+2*math.pi/3)))
    #screen.blit(orb_img, (300 + 30*math.cos(time+4*math.pi/3), 300 + 30*math.sin(time+4*math.pi/3)))
    screen.blit(invader(), (WIDTH/2, HEIGHT/2))
    clock.tick(80)
    pygame.display.update()