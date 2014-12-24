__author__ = 'justin'
import pygame

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
B_GREEN = (0,255,0)


def draw():
    image = pygame.Surface([20, 20])
    pygame.draw.rect(image, (61, 136, 3), (0, 0, 20, 20))
    pygame.draw.rect(image, B_GREEN, (8, 2, 4, 16))
    pygame.draw.rect(image, B_GREEN, (2, 8, 16, 4))
    return image

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    screen.fill((255,255,255))
    screen.blit(draw(),(WIDTH/2,HEIGHT/2))

    pygame.display.update()