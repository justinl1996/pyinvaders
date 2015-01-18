__author__ = 'justin'
import pygame
import colour
import math

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


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill((255, 255, 255))
    screen.blit(speedboost(), (WIDTH/2, HEIGHT/2))

    clock.tick(80)
    pygame.display.update()