from data import interface, colour

__author__ = 'justin'
import pygame


class MenuSelect(object):
    def __init__(self, text, func, font_size):
        self._font = pygame.font.Font('font/ka1.ttf', font_size)
        self._text = text
        self._func = func
        self._image = self._init_text()
        self._status = 0
        self._mark = False

    def _init_text(self):
        text = self._font.render(self._text, True, colour.GREEN)
        return text

    def get_image(self):
        """Returns the text surface"""
        return self._image

    def set_notselected(self):
        """Set the text colour to be unselected, unless it has been previously marked (white colour)"""
        if self._mark:
            self._image = self._font.render(self._text, True, colour.GREY)
        else:
            self._status = 0
            self._image = self._font.render(self._text, True, colour.GREEN)

        return self

    def set_selected(self):
        """Set the text colour to be selected (blue colour)"""
        self._status = 1
        self._image = self._font.render(self._text, True, colour.BLUE)
        return self

    def mark_selection(self):
        """Greys out the text"""
        self._mark = True
        self._image = self._font.render(self._text, True, colour.GREY)

    def get_mark(self):
        """Returns true if the menuitem has been marked"""
        return self._mark

    def unmark(self):
        """Set the text colour to be unselected and unmarks it if it has not already been"""
        if self._mark:
            self._mark = False
            self._image = self._font.render(self._text, True, colour.GREEN)
            return True
        else:
            return False

    def make_selection(self):
        """Executes the function and passes the return value to caller"""
        return self._func()

class BasicMenu(object):
    def __init__(self, menuitems, s_loc, sound):
        self._screen = pygame.display.get_surface()
        self._v_spacing = int(self._screen.get_height()*0.1)
        self._menuitems = menuitems
        self._s_loc = s_loc     #location on screen by ratio
        self._topleft = (s_loc[0]*self._screen.get_width(), s_loc[1]*self._screen.get_height()/2)
        self._sel = [0, 0]
        self.sound = sound
        self._mark = []


    def set_first(self, sel):
        """Sets the first selection to be selected"""
        self._sel = sel
        self._menuitems[self._sel[1]][self._sel[0]].set_selected()

    def set_defaults(self, lst):
        """Takes a list of tuples containing the row and column index (0 based) and sets them to be marked
        Precondition: lst must contain valid index values"""
        for i in lst:
            self._menuitems[i[1]][i[0]].mark_selection()
            self._menuitems[i[1]][i[0]].make_selection()
            self._mark.append(i)

    def clear_selections(self):
        """Clears all marked selections, setting them to their default colour"""
        for i in self._mark:
            self._menuitems[i[1]][i[0]].unmark()
            self._mark = []

    def get_settings(self):
        """Returns a list containing the selections which have been marked"""
        return self._mark

    def reset(self):
        """Call to reset positioning of menu after screen size is reset"""
        self._screen = pygame.display.get_surface()
        self._topleft = (self._s_loc[0]*self._screen.get_width(), self._s_loc[1]*self._screen.get_height())
        self._v_spacing = int(self._screen.get_height()*0.1)


    def _draw_items(self):
        """Draws the selections and titles to screen"""
        startx, starty = self._topleft[0], self._topleft[1]
        for i, y in enumerate(self._menuitems):
            #self._textob[i].render(self._titles[i])
            prev = startx
            for x, text in enumerate(y):
                img = text.get_image()
                self._screen.blit(img, (prev, starty + i*self._v_spacing))
                prev += img.get_width() + 40

    def move_up(self, dir):
        """Moves the position of menu selection up (dir=1) or down (dir=-1)"""
        self._menuitems[self._sel[1]][self._sel[0]].set_notselected()

        self._sel[1] -= dir
        if self._sel[1] < 0:
            self._sel[1] = len(self._menuitems) - 1
        elif self._sel[1] == len(self._menuitems):
            self._sel[1] = 0
        if self._sel[0] >= len(self._menuitems[self._sel[1]]):
            self._sel[0] = len(self._menuitems[self._sel[1]]) - 1
        self._menuitems[self._sel[1]][self._sel[0]].set_selected()

    def move_across(self, dir):
        """Moves the position of menu selection across (right=1) or (left=-1)"""
        self._menuitems[self._sel[1]][self._sel[0]].set_notselected()
        self._sel[0] += dir
        if self._sel[0] < 0:
            self._sel[0] = len(self._menuitems[self._sel[1]]) - 1
        elif self._sel[0] == len(self._menuitems[self._sel[1]]):
            self._sel[0] = 0
        self._menuitems[self._sel[1]][self._sel[0]].set_selected()

    def run(self):
        if self._sel[1] != len(self._menuitems) - 1:
            for i, item in enumerate(self._menuitems[self._sel[1]]):
                if item.unmark():
                    self._mark.remove([i, self._sel[1]])
            self._menuitems[self._sel[1]][self._sel[0]].mark_selection()
            self._mark.append(self._sel[:])
        return self._menuitems[self._sel[1]][self._sel[0]].make_selection()

    def update(self):
        self._draw_items()



class OptionList(BasicMenu):
    def __init__(self, menuitems, titles, topleft, sound):
        BasicMenu.__init__(self, menuitems, topleft, sound)
        self._titles = titles
        self._textob = []
        self._init_text()

    def _init_text(self):
        """Initialize the titles"""
        self._textob = [interface.ArcadeText(self._topleft[0], (self._topleft[1] - 25) + i*self._v_spacing, 20, colour.SILVER)
                        for i in range(len(self._titles))]

    def reset(self):
        """Call to reset positioning"""
        self._screen = pygame.display.get_surface()
        self._topleft = (int(self._s_loc[0]*self._screen.get_width()), int(self._s_loc[1]*self._screen.get_height()))
        self._v_spacing = int(self._screen.get_height()*0.1)
        self._init_text()


    def _draw_items(self):
        """Draws the selections and titles to screen"""
        startx, starty = self._topleft[0], self._topleft[1]
        for i, y in enumerate(self._menuitems):
            self._textob[i].render(self._titles[i])
            prev = startx
            for x, text in enumerate(y):
                img = text.get_image()
                self._screen.blit(img, (prev, starty + i*self._v_spacing))
                prev += img.get_width() + 40

class MenuList(object):
    def __init__(self, menuitems, s_loc, sound):
        self._screen = pygame.display.get_surface()
        self._menuitems = menuitems
        self._s_loc = s_loc
        self._topleft = self._topleft = (s_loc[0]*self._screen.get_width(), s_loc[1]*self._screen.get_height()/2)
        self._sel = 0
        self.sound = sound
        self._menuitems[self._sel].set_selected()

    def reset(self):
        """Call to reset positioning"""
        self._screen = pygame.display.get_surface()
        self._topleft = (int(self._s_loc[0]*self._screen.get_width()), int(self._s_loc[1]*self._screen.get_height()))

    def _draw_items(self):
        startx, starty = self._topleft[0], self._topleft[1]
        for i, text in enumerate(self._menuitems):
            self._screen.blit(text.get_image(), (startx, starty + i*70))

    def move_up(self, dir):
        self._menuitems[self._sel].set_notselected()
        self._sel -= dir
        if self._sel < 0:
            self._sel = len(self._menuitems) - 1
        elif self._sel == len(self._menuitems):
            self._sel = 0
        self._menuitems[self._sel].set_selected()

    def run(self):
        return self._menuitems[self._sel].make_selection()

    def update(self):
        self._draw_items()