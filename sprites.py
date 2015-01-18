__author__ = 'justin'
import pygame
import colour
"""This file contains all the functions required to draw the sprites"""



def ship():
    """The player's ship"""
    image = pygame.Surface([50, 15], pygame.SRCALPHA)
    pygame.draw.rect(image, colour.RED, (15, 0, 20, 15))
    pygame.draw.polygon(image, colour.BLUE, [(50, 15), (35, 25), (35, 0)])
    pygame.draw.polygon(image, colour.BLUE, [(0, 15), (15, 0), (15, 15)])
    return image

def rocket():
    """Rocket weapon"""
    image = pygame.Surface([16,30], pygame.SRCALPHA)
    pygame.draw.circle(image, colour.GREY, (8, 8), 8, 0)
    pygame.draw.rect(image, colour.GREY, (0, 8, 16, 22))
    pygame.draw.rect(image, colour.RED, (0, 20, 16, 5))
    return image

def healthpack():
    """Healthpack drop"""
    image = pygame.Surface([20, 20])
    image.fill((61, 136, 3))
    pygame.draw.rect(image, colour.B_GREEN, (8, 2, 4, 16))
    pygame.draw.rect(image, colour.B_GREEN, (2, 8, 16, 4))
    return image

def rocketdrop():
    """Rocket weapon drop"""
    image = pygame.Surface((20, 20))
    image.fill(colour.SILVER)
    pygame.draw.rect(image, colour.BLACK, (5, 6, 10, 12))
    pygame.draw.circle(image, colour.BLACK, (10, 6), 5, 0)
    return image

def ammopack():
    """Ammunition drop icon"""
    image = pygame.Surface([18, 20], pygame.SRCALPHA)
    for n in range(0, 3):
        temp = pygame.Surface([6, 20], pygame.SRCALPHA)
        pygame.draw.circle(temp, colour.GOLD, (3, 3), 3, 1)
        pygame.draw.circle(temp, colour.GOLD, (3, 3), 3, 0)
        pygame.draw.rect(temp, colour.J_GREEN, (0, 4, 6, 16))
        image.blit(temp, (n*6, 0))
    return image

def dual_bullet():
    """Dual Bullet Icon used in the top interface"""
    text = pygame.font.SysFont('arial', 10).render("x2", True, (0, 0, 0))
    image = pygame.Surface((20, 20))
    image.fill(colour.SILVER)
    image.blit(text, (9, 6))
    pygame.draw.rect(image, colour.RED, (2, 4, 2, 12))
    pygame.draw.rect(image, colour.RED, (6, 4, 2, 12))
    return image

def bullet_icon():
    """Bullet Icon used in the top interface"""
    font_ob = pygame.font.SysFont('arial', 12)
    text = font_ob.render("x1", True, (0, 0, 0))
    image = pygame.Surface((20, 20))
    image.fill(colour.SILVER)
    image.blit(text, (7, 5))
    pygame.draw.rect(image, colour.RED, (2, 4, 2, 12))
    #image = pygame.transform.smoothscale(image, (100, 100))
    #image = pygame.transform.scale(image, (25, 25))
    return image

def startweapon():
    """Draws starting weapon"""
    image = pygame.Surface([6, 6], pygame.SRCALPHA)
    pygame.draw.circle(image, colour.BLUE, (3, 3), 3, 0)
    return image

def startweponicon():
    """Draws the icon representing the starting weapon"""
    image = pygame.Surface([20, 20])
    image.fill(colour.SILVER)
    pygame.draw.circle(image, colour.BLUE, (10, 10), 4, 0)
    return image

def speedboost():
    """Draws the item drop for the speed boost"""
    image = pygame.Surface([20, 20])
    image.fill(colour.SILVER)
    pygame.draw.polygon(image, colour.YELLOW, [(0, 15), (10, 4), (20, 15)])
    pygame.draw.polygon(image, colour.SILVER, [(0, 19), (10, 9), (20, 19)])
    return image

#WEAPON_ICON = {"bullet": bullet_icon(),"rocket": rocketdrop(),"dual":dual_bullet()}