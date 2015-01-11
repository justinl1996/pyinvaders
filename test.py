__author__ = 'justin'
import pygame
import colour

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


def draw_health():
    image = pygame.Surface((20, 20), flags=pygame.SRCALPHA, depth=32)
    image.fill((61, 136, 3))
    pygame.draw.rect(image, colour.B_GREEN, (8, 2, 4, 16))
    pygame.draw.rect(image, colour.B_GREEN, (2, 8, 16, 4))
    return image

def draw_bullet():
    image = pygame.Surface([6, 20], pygame.SRCALPHA)
    pygame.draw.circle(image, colour.GOLD, (3, 3), 3, 1)
    pygame.draw.circle(image, colour.GOLD, (3, 3), 3, 0)
    pygame.draw.circle(image, colour.GOLD, (3, 17), 3, 0)
    pygame.draw.rect(image, colour.J_GREEN, (0, 4, 6, 14))
    return image

def draw_rocket():
    image = pygame.Surface([16,30], pygame.SRCALPHA)
    pygame.draw.circle(image, colour.BLACK, (8, 8), 8, 0)
    pygame.draw.rect(image, colour.BLACK, (0, 8, 16, 22))
    return image

def draw_ship():
    image = pygame.Surface([50, 15], pygame.SRCALPHA)
    pygame.draw.rect(image, colour.RED, (15, 0, 20, 15))
    pygame.draw.polygon(image, colour.BLUE, [(50, 15), (35, 25), (35, 0)])
    pygame.draw.polygon(image, colour.BLUE, [(0, 15), (15, 0), (15, 15)])
    return image

def draw_rocketDrop():
    image = pygame.Surface((20, 20))
    image.fill(colour.SILVER)
    pygame.draw.rect(image, colour.BLACK, (5, 6, 10, 12))
    pygame.draw.circle(image, colour.BLACK, (10, 6), 5, 0)
    return image

def draw_dual():
    font_ob = pygame.font.SysFont('arial', 10)
    text = font_ob.render("x2", True, (0, 0, 0))
    image = pygame.Surface((20, 20))
    image.fill(colour.SILVER)
    image.blit(text, (9, 6))
    pygame.draw.rect(image, colour.RED, (2, 4, 2, 12))
    pygame.draw.rect(image, colour.RED, (6, 4, 2, 12))
    return image

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill((255, 255, 255))
    #screen.blit(draw_health(),(WIDTH/2,HEIGHT/2))
    #screen.blit(draw_bullet(), (WIDTH/2, HEIGHT/2))
    #screen.blit(draw_ship(), (WIDTH/2, HEIGHT/2))
    screen.blit(draw_dual(), (WIDTH/2, HEIGHT/2))
    pygame.display.update()