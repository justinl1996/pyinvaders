__author__ = 'justin'
import pygame
import time
import random
import interface

RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
B_GREEN = (0, 255, 0)
BLUE = (120, 120, 230)
D_BLUE = (120, 120, 100)
GOLD = (109, 109, 17)
J_GREEN = (78, 101, 65)

class Ship(pygame.sprite.Sprite):
    """Class which represents the player's ship"""
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = pygame.Surface([width,height])
        pygame.draw.rect(self.image, RED, (0,0,width,height))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.y = 0.92*self.screen.get_rect()[3]
        self.rect.x = (self.screen.get_rect()[2] - self.width)/2
        self._health = 100  #Starting health
        self._ammo = 100    #Starting ammo
        self._score = 0

    def right(self, amount):
        """Moves the ship in the right direction"""
        if self.rect.x + self.width < self.screen.get_rect()[2]:
            self.rect.x += amount

    def left(self, amount):
        """Moves the ship in the left direction"""
        if self.rect.x > 0:
            self.rect.x -= amount

    def shoot(self):
        if self._ammo > 0:
            self._ammo -= 1
            return Bullet(self.rect.x+self.width/2, self.rect.y + self.height, 3)

    def get_health(self):
        """Returns the amount of health remaining"""
        return self._health

    def take_damage(self, amount):
        """Decrement the health of the ship by a given amount"""
        self._health -= amount

    def add_health(self, amount):
        """Increment the health of the ship by a given amount"""
        if amount + self._health <= 100:
            self._health += amount

    def get_ammo(self):
        """Returns the amount of ammo remaining"""
        return self._ammo

    def add_ammo(self, amount):
        """Increments the player's ammunition"""
        if self._ammo + amount < 150:
            self._ammo += amount
        else:
            self._ammo = 150

    def decrement_ammo(self, amount):
        self._ammo -= amount

    def update_score(self, amount):
        """updates the score of the ship, 10 per-kill"""
        self._score += amount

    def get_score(self):
        """Returns the score"""
        return self._score


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = self._draw_bullet(RED)
        self.rect = self.image.get_rect()
        self.rect.y = y-25
        self.rect.x = x
        self.speed = speed
        #pygame.mixer.Sound("Laser.wav").play()

    def _draw_bullet(self, colour):
        """Draws the bullet shape onto the surface. Returns the surface"""
        image = pygame.Surface([2, 12])
        pygame.draw.rect(image, colour, (0, 0, 2, 12))
        return image

    def update(self):
        """Updates position of bullet i.e. moves it up the screen. If it moves off the screen it is automatically destroyed"""
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

    def gety(self):
        """Returns the y-value of the sprite"""
        return self.rect.y

class BulletDown(Bullet):
    """Class BulletUp inherits from Bullet. The method 'update' has been modified to move the bullet down"""

    def __init__(self, x, y, speed):
        Bullet.__init__(self, x, y, speed)
        self.image = self._draw_bullet(D_BLUE)

    def update(self):
        """Updates position of bullet, i.e. moves it down. If it moves off the screen it is automatically destroyed"""
        self.rect.y += self.speed
        if self.rect.y > self.screen.get_rect()[3]:
            self.kill()

class HealthPack(BulletDown):
    """Class HealthPack inherits from BulletDown"""
    def _draw_bullet(self, colour):
        """Draws a health pack"""
        image = pygame.Surface([20, 20])
        #pygame.draw.rect(image, B_GREEN, (7, 4, 13, 16))
        #pygame.draw.rect(image, B_GREEN, (4, 7, 16, 13))
        pygame.draw.rect(image, (61, 136, 3), (0, 0, 20, 20))
        pygame.draw.rect(image, B_GREEN, (8, 2, 4, 16))
        pygame.draw.rect(image, B_GREEN, (2, 8, 16, 4))
        return image

    def __str__(self):
        return "health"

class AmmoPack(BulletDown):
    """Class AmmoPack inherits from BulletDown"""

    def _draw_bullet(self, colour):
        image = pygame.Surface([18, 20], pygame.SRCALPHA)
        for n in range(0, 3):
            temp = pygame.Surface([6, 20], pygame.SRCALPHA)
            pygame.draw.circle(temp, GOLD, (3, 3), 3, 1)
            pygame.draw.circle(temp, GOLD, (3, 3), 3, 0)
            pygame.draw.rect(temp, J_GREEN, (0, 4, 6, 16))
            image.blit(temp, (n*6, 0))
        return image

    def __str__(self):
        return "ammo"

class EnemyCluster(object):
    """ This class groups together enemy ships, it is automatically populated"""
    def __init__(self, draw_screen):
        self.screen = pygame.display.get_surface()
        self.enemies = pygame.sprite.Group()
        self.health_bars = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self._populate()
        self.direction = 1 # 1=right, -1=left
        self.diry = 0 # 1=down 0=no vertical movement
        self.screen = draw_screen
        self.center = self.screen.get_rect()[2]/2
        self.old_time = time.clock()

    def get_ships(self):
        """Returns the group of enemy ships contained in this cluster"""
        return self.enemies

    def get_items(self):
        """Returns the group of items"""
        return self.items

    def get_bullets(self):
        """Returns the group of bullets"""
        return self.bullets

    def _populate(self):
        """Populates the cluster with the enemy battleships"""
        width = self.screen.get_rect()[2]
        height = self.screen.get_rect()[3]
        left = 0.1*width
        right = width - left

        for x in range(int(left), int(right), 80):
            for y in range(int(0.1*height),height/2, 40):
                temp = Enemy(x, y, 30, 30, pygame.mixer.Sound("Blast.wav"), self)
                self.health_bars.add(interface.HealthBar(temp, x, y, 30, 4))
                self.enemies.add(temp)

    def _shoot(self):
        """Randomly selects a ship from the group and calls its shoot method"""
        if time.clock() - self.old_time > 0.08:
            print "Selecting random ship"
            select = random.randint(0, len(self.enemies.sprites())-1)
            self.bullets.add(self.enemies.sprites()[select].shoot())
            self.old_time = time.clock()

    def _move_ships(self):
        """Updates the ship's position"""
        for ship in self.enemies.sprites():
            ship.move(self.direction, self.diry)
        self.diry = 0

    def _move_health(self):
        """Moves the heathbars, call this to update their position after enemy ships have moved"""
        for h in self.health_bars:
            h.move()

    def update(self):
        if self.direction == 1:
            if self.center > 0.60*self.screen.get_rect()[2]:
                self.direction = -1
                self.diry = 5
        else:
            if self.center < 0.45*self.screen.get_rect()[2]:
                self.direction = 1
                self.diry = 5

        self.center += self.direction
        self._move_ships()
        self._move_health()
        self.enemies.draw(self.screen)
        self.health_bars.draw(self.screen)
        self.bullets.update()
        self.bullets.draw(self.screen)
        self.items.update()
        self.items.draw(self.screen)
        self._shoot()

class Enemy(pygame.sprite.Sprite):
    """This class represents the enemy sprites"""
    def __init__(self, x, y, width, height, destroy_snd, parent):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.screen = pygame.display.get_surface()
        pygame.draw.rect(self.image, BLUE, (0,0,width,height))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.width = width
        self.height = height
        self.health = 10
        self.destroy_snd = destroy_snd
        self.parent = parent

    def destroy(self):
        """Plays the destruction sound of the enemy ship, returns true if enemy is destroyed"""
        self.health -= 5
        if self.health <= 0:
            self.destroy_snd.play()
            self.kill()
            ran = random.randint(1, 5)
            if ran == 1:
                self.parent.items.add(HealthPack(self.rect.x, self.rect.y, 2))
            elif ran == 2 or ran == 3:
                self.parent.items.add(AmmoPack(self.rect.x, self.rect.y, 2))
            return True

        return False

    def move(self, dirx, diry=0):
        """Moves the enemy ship and associated healthbar in either the x and/or the y direction"""
        self.rect.x += dirx
        self.rect.y += diry
        #self.health.move(self.rect.x, self.rect.y+self.height+2)

    def getx(self):
        """Return the x coordinate of the enemy ship"""
        return self.rect.x

    def gety(self):
        """Return the y coordinate of the enemy ship"""
        return self.rect.y

    def shoot(self):
        """Shoots a bullet ie. Returns a bullet with start coordinate same as self"""
        return BulletDown(self.rect.x+self.width/2, self.rect.y + self.height, 3)

    def get_health(self):
        """Returns the amount of a health"""
        return self.health


