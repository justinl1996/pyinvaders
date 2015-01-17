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

hello = ScrollText(500, 500, 10, "Hello")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill((255, 255, 255))
    hello.move_y(-1)
    #screen.blit(draw_health(),(WIDTH/2,HEIGHT/2))
    #screen.blit(draw_bullet(), (WIDTH/2, HEIGHT/2))
    #screen.blit(draw_ship(), (WIDTH/2, HEIGHT/2))
    #screen.blit(_draw_bullet(), (WIDTH/2, HEIGHT/2))
    #screen.blit(pygame.transform.rotate(_draw_bullet(), -120), (WIDTH/2, HEIGHT/2))
    #screen.blit(startIcon(), (WIDTH/2, HEIGHT/2))
    #screen.blit(img, (WIDTH/2, HEIGHT/2))

    clock.tick(80)
    pygame.display.update()