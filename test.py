__author__ = 'justin'
import pygame

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
B_GREEN = (0, 255, 0)
GREY = (109, 109, 109)
L_GREY = (182, 182, 182)
GOLD = (109, 109, 17)
J_GREEN = (78, 101, 65)

def draw_health():
    image = pygame.Surface((50, 50), flags=pygame.SRCALPHA, depth=32)
    pygame.draw.rect(image, (61, 136, 3), (0, 0, 20, 20))
    pygame.draw.rect(image, B_GREEN, (8, 2, 4, 16))
    pygame.draw.rect(image, B_GREEN, (2, 8, 16, 4))
    return image

def draw_bullet():
    image = pygame.Surface([6, 20], pygame.SRCALPHA)
    pygame.draw.circle(image, GOLD, (3, 3), 3, 1)
    pygame.draw.circle(image, GOLD, (3, 3), 3, 0)
    pygame.draw.circle(image, GOLD, (3, 17), 3, 0)
    pygame.draw.rect(image, J_GREEN, (0, 4, 6, 14))
    return image

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill((255, 255, 255))
    #screen.blit(draw_health(),(WIDTH/2,HEIGHT/2))
    screen.blit(draw_bullet(), (WIDTH/2, HEIGHT/2))
    pygame.display.update()