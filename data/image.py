__author__ = 'justin'
import pygame

class Image():
    """Class for loading and rendering imported images"""
    def __init__(self, file, x, y):
        self.img = pygame.image.load(file)
        self.screen = pygame.display.get_surface()
        self.x = x - self.img.get_width()/2
        self.y = y - self.img.get_height()/2

    def reset_pos(self, newx, newy):
        """Resets the  x, y coordinates to blit the surface"""
        self.x = newx - self.img.get_width()/2
        self.y = newy - self.img.get_height()/2

    def render(self):
        """Draw the surface on screen"""
        self.screen.blit(self.img, (self.x, self.y))




