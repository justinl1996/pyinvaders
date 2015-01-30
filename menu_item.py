__author__ = 'justin'
import pygame
import colour
import sprites

class MenuSelect(object):
    def __init__(self, text, func, font_size):
        self._font = pygame.font.SysFont('arial', font_size)
        self._text = text
        self._func = func
        self._image = self._init_text()
        self._col = (colour.WHITE, colour.BLUE)
        self._status = 0


    def _init_text(self):
        text = self._font.render(self._text, True, colour.WHITE)
        sw = pygame.Surface((text.get_width()+40, text.get_height()), pygame.SRCALPHA)
        sw.blit(text, (40, 0))
        return sw

    def get_image(self):
        """Returns the text surface"""
        return self._image

    def change_selection(self):
        """alternates the text colour from default to selected and plays sound"""

        if self._status == 1:
            self._status = 0
            text = self._font.render(self._text, True, self._col[0])
            self._image = pygame.Surface((text.get_width()+40, text.get_height()+5), pygame.SRCALPHA)
        else:
            self._status = 1
            text = self._font.render(self._text, True, self._col[1])
            self._image = pygame.Surface((text.get_width()+40, text.get_height()+5), pygame.SRCALPHA)
            self._image.blit(pygame.transform.rotate(sprites.ship(), -90), (0, 0))
        self._image.blit(text, (40, 0))
        return self

    def make_selection(self):
        """Executes the function and pass the return value to caller"""
        return self._func()