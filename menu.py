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
        self.option_titles = ["Resolution", "Invader Colour", "Sound", "Apply Settings?"]
        self.options = [[menu_item.MenuSelect("1024x768", lambda: self.screen_reset(1024, 768), 30),
                         menu_item.MenuSelect("1280x1024", lambda: self.screen_reset(1280, 1024), 30),
                        menu_item.MenuSelect("1278x720", lambda: self.screen_reset(1278, 720), 30)],
                        [menu_item.MenuSelect("blue", lambda: self._set_invader_col(colour.BLUE), 30),
                         menu_item.MenuSelect("red", lambda: self._set_invader_col(colour.RED), 30),
                         menu_item.MenuSelect("purple", lambda: self._set_invader_col(colour.PURPLE), 30)],
                        [menu_item.MenuSelect("ON", lambda: self._sound(True), 30),
                        menu_item.MenuSelect("OFF", lambda: self._sound(False), 30)],
                        [menu_item.MenuSelect("OK", self._options_OK, 30),
                         menu_item.MenuSelect("Cancel", self._options_cancel, 30)]]
        self.s_width = SCREEN_SIZE[0]
        self.s_height = SCREEN_SIZE[1]
        self.main_topleft = (int(self.s_width*0.1), int(self.s_height*0.60))
        self.opt_topleft = (int(self.s_width*0.4), int(self.s_height*0.60))
        self.sound = interface.SoundEffects()
        self.option_menu = menu_item.OptionList(self.options, self.option_titles, self.opt_topleft, self.sound)
        self.main_menu = menu_item.MenuList(self.text, self.main_topleft, self.sound)
        self._opt_settings = [[0, 0], [0, 1], [0, 2]]
        self.option_menu.set_defaults(self._opt_settings)
        self.stars = []
        self._bg_init()
        self._enemy_col = colour.BLUE
        self.option_on = False


    def _bg_init(self):
        """Populate a list containing white pixel at random locations with random speed
        call to initialize background after screen dimensions have been reset
        """
        self.stars = [[random.randrange(0, self.s_width-1), random.randrange(0, self.s_height-1),
                       random.randrange(1, 4)] for _ in range(256)]

    def screen_reset(self, width, height):
        """Resets the video display"""
        pygame.display.set_mode((width, height))
        self.s_width = width
        self.s_height = height
        self.main_menu.reset(int(self.s_width*0.1), int(self.s_height*0.60))
        self.option_menu.reset(int(self.s_width*0.4), int(self.s_height*0.60))
        self._bg_init()


    def _bg_update(self):
        """Redraws the background, run this prior to drawing game objects"""
        self.screen.fill(colour.BLACK)
        for star in self.stars:
            if star[2] + star[1] > self.s_height:
                star[1] = 0
            else:
                star[1] += star[2]
            self.screen.set_at((star[0], star[1]), colour.WHITE)

    def _play(self):
        print "PLAY"

    def _instructions(self):
        pass

    def _options(self):
        self.option_on = True

    def _sound(self, setting):
        self.sound.set_on(setting)

    def _set_invader_col(self, col):
        self._enemy_col = col

    def _options_OK(self):
        self.option_on = False
        #self.option_menu.clear_selections()
        #print self.option_menu.get_settings()
        self._opt_settings = self.option_menu.get_settings()

    def _options_cancel(self):
        self.option_on = False
        self.option_menu.clear_selections()
        self.option_menu.set_defaults(self._opt_settings)

    def _exit(self):
        raise SystemExit

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.sound.play_select()
                        if self.option_on:
                            self.option_menu.move_up(1)
                        else:
                            self.main_menu.move_up(1)
                    elif event.key == pygame.K_DOWN:
                        self.sound.play_select()
                        if self.option_on:
                            self.option_menu.move_up(-1)
                        else:
                            self.main_menu.move_up(-1)
                    elif event.key == pygame.K_LEFT and self.option_on:
                        self.sound.play_select()
                        self.option_menu.move_across(-1)
                    elif event.key == pygame.K_RIGHT and self.option_on:
                        self.sound.play_select()
                        self.option_menu.move_across(1)
                    elif event.key == pygame.K_RETURN:
                        if self.option_on:
                            self.option_menu.run()
                        else:
                            self.main_menu.run()
            self._bg_update()
            if self.option_on:
                self.option_menu.update()
            self.main_menu.update()
            pygame.display.update()


if __name__ == '__main__':
    app = Main()
    app.run()
