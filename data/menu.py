import pygame
from data import colour
from data import menu_item
from data import interface
from data import game
from data import image
from data import score

SCREEN_SIZE = [1024, 768]

class Menu(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.s_width = SCREEN_SIZE[0]
        self.s_height = SCREEN_SIZE[1]
        self._bg = interface.StarBackground()
        self.sound = interface.SoundEffects()
        self._instruction_on = False
        self._option_on = False
        self._title = image.Image("img/title.png", self.s_width/2, 0.25*self.s_height)
        self._instruction = image.Image("img/controls.png", self.s_width*0.6, 0.75*self.s_height)
        self._info = interface.Info(1.1)
        self._menu_init()
        self._enemy_col = colour.BLUE

    def _menu_init(self):
        text = [menu_item.MenuSelect("Play", self._play, 30),
                     menu_item.MenuSelect("Instructions", self._instructions, 30),
                     menu_item.MenuSelect("Highscores", self._high_scores, 30),
                     menu_item.MenuSelect("Options", self._options, 30),
                     menu_item.MenuSelect("Exit", self._exit, 30),]
        option_titles = ["Resolution", "Invader Colour", "Sound", "Apply Settings?"]
        options = [[menu_item.MenuSelect("1024x768", lambda: self.screen_reset(1024, 768), 20),
                         menu_item.MenuSelect("1280x1024", lambda: self.screen_reset(1280, 1024), 20),
                        menu_item.MenuSelect("1278x720", lambda: self.screen_reset(1278, 720), 20)],
                        [menu_item.MenuSelect("blue", lambda: self._set_invader_col(colour.BLUE), 20),
                         menu_item.MenuSelect("red", lambda: self._set_invader_col(colour.RED), 20),
                         menu_item.MenuSelect("purple", lambda: self._set_invader_col(colour.PURPLE), 20),
                         menu_item.MenuSelect("green", lambda: self._set_invader_col(colour.GREEN), 20)],
                        [menu_item.MenuSelect("ON", lambda: self._sound(True), 20),
                        menu_item.MenuSelect("OFF", lambda: self._sound(False), 20)],
                        [menu_item.MenuSelect("OK", self._options_OK, 20),
                         menu_item.MenuSelect("Cancel", self._options_cancel, 20)]]
        instructions = [[menu_item.MenuSelect("OK", self._instruction_OK, 20)]]
        self._instruction_menu = menu_item.BasicMenu(instructions, (0.8, 0.8), 50, 40)
        self._option_menu = menu_item.OptionList(options, option_titles, (0.4, 0.6), 50, 70)
        self.main_menu = menu_item.MenuList(text, (0.1, 0.5))
        self._instruction_menu.set_first([0, 0])
        self._opt_settings = [[0, 0], [0, 1], [0, 2]]
        self._option_menu.set_defaults(self._opt_settings)
        self._option_menu.set_first([0, 0])

    def screen_reset(self, width, height):
        """Resets the video display"""
        pygame.display.set_mode((width, height))
        self.s_width = width
        self.s_height = height
        self.main_menu.reset()
        self._option_menu.reset()
        self._instruction_menu.reset()
        self._title.reset_pos(self.s_width/2, self.s_height*0.25)
        self._info.screen_init()
        self._bg.init_bg()


    def _bg_update(self):
        """Redraws the background, run this prior to drawing game objects"""
        self.screen.fill(colour.BLACK)
        for star in self._stars:
            if star[2] + star[1] > self.s_height:
                star[1] = 0
            else:
                star[1] += star[2]
            self.screen.set_at((star[0], star[1]), colour.WHITE)

    def _play(self):
        game.Game(self.screen, self.sound, self._enemy_col).run()

    def _instructions(self):
        self._option_on = False
        self._instruction_on = True

    def _high_scores(self):
        score.ScoreScreen(self.sound).high_score()

    def _options(self):
        self._instruction_on = False
        self._option_on = True

    def _sound(self, setting):
        self.sound.set_on(setting)

    def _set_invader_col(self, col):
        self._enemy_col = col

    def _instruction_OK(self):
        self._instruction_on = False

    def _options_OK(self):
        self._option_on = False
        self._opt_settings = self._option_menu.get_settings()

    def _options_cancel(self):
        self._option_on = False
        self._option_menu.clear_selections()
        self._option_menu.set_defaults(self._opt_settings)

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
                        if self._option_on:
                            self._option_menu.move_up(1)
                        elif self._instruction_on:
                            self._instruction_menu.move_up(1)
                        else:
                            self.main_menu.move_up(1)
                    elif event.key == pygame.K_DOWN:
                        self.sound.play_select()
                        if self._option_on:
                            self._option_menu.move_up(-1)
                        elif self._instruction_on:
                            self._instruction_menu.move_up(-1)
                        else:
                            self.main_menu.move_up(-1)
                    if event.key == pygame.K_LEFT and self._option_on:
                        self.sound.play_select()
                        self._option_menu.move_across(-1)
                    elif event.key == pygame.K_RIGHT and self._option_on:
                        self.sound.play_select()
                        self._option_menu.move_across(1)
                    elif event.key == pygame.K_RETURN:
                        if self._option_on:
                            self._option_menu.run()
                        elif self._instruction_on:
                            self._instruction_menu.run()
                        else:
                            self.main_menu.run()
            self._bg.update()
            self._title.render()

            if self._option_on:
                self._option_menu.update()
            elif self._instruction_on:
                self._instruction_menu.update()
                self._instruction.render()

            self._info.render()
            self.main_menu.update()
            self.clock.tick(80)
            pygame.display.update()



