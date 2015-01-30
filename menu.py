import pygame
import random
import colour
import menu_item
import sprites
import interface

SCREEN_SIZE = [1024, 768]

class Main(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.text = [menu_item.MenuSelect("Play", self._play, 40),
                     menu_item.MenuSelect("Instructions", self._instructions, 40),
                     menu_item.MenuSelect("Options", self._options, 40),
                     menu_item.MenuSelect("Exit", self._exit, 40)]
        self.text[0].change_selection()
        self.ship_icon = sprites.ship()
        self.sel = 0
        self.s_width = SCREEN_SIZE[0]
        self.s_height = SCREEN_SIZE[1]
        self.topleft = (self.s_width*0.1, self.s_height*0.60)
        self.spacing = 70
        self.stars = [[random.randrange(0, self.s_width-1), random.randrange(0, self.s_height-1),
                       random.randrange(0, 3)] for _ in range(256)]
        self.sound = interface.SoundEffects()

    def _bg_update(self):
        """Redraws the background, run this prior to drawing game objects"""
        self.screen.fill(colour.BLACK)
        for star in self.stars:
            if star[2] + star[1] > self.s_height:
                star[1] = 0
            else:
                star[1] += star[2]
            self.screen.set_at((star[0], star[1]), colour.WHITE)

    def _draw_text(self):
        """Blits the text surfaces contained in self.text_select on screen"""
        for i, text in enumerate(self.text):
            self.screen.blit(text.get_image(), (self.topleft[0], self.topleft[1] + i*self.spacing))

    def _change_selection(self, dir):
        """Call this to trigger a selection change in the menu"""
        self.sound.play_select()
        self.text[self.sel] = self.text[self.sel].change_selection()
        self.sel += dir
        if self.sel == -1:
            self.sel = len(self.text) - 1
        elif self.sel == len(self.text):
            self.sel = 0
        self.text[self.sel] = self.text[self.sel].change_selection()


    def _play(self):
        pass

    def _instructions(self):
        pass

    def _options(self):
        pass

    def _exit(self):
        raise SystemExit

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._change_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        self._change_selection(1)
                    elif event.key == pygame.K_RETURN:
                        self.sound.play_destroy("bullet")
                        self.text[self.sel].make_selection()

            self._bg_update()
            self._draw_text()
            pygame.display.update()


if __name__ == '__main__':
    app = Main()
    app.run()
