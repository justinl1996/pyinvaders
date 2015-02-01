__author__ = 'justin'
import pygame
import time
import random
import interface
import colour
import sprites
import math
import vector

class Ship(pygame.sprite.Sprite):
    """Class which represents the player's ship"""
    def __init__(self, sound):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = sprites.ship()
        self.rect = self.image.get_rect()
        self.rect.y = 0.92*self.screen.get_rect()[3]
        self.height = 15
        self.width = 50
        self.rect.x = (self.screen.get_rect()[2] - self.width)/2
        self._health = 100  #Starting health
        self._ammo_limits = {"bullet": 120, "rocket": 7, "spread": 150}  #Ammo limits
        self._ammo = {"bullet": 100, "rocket": 5, "spread": 80}    #Starting ammo
        self._score = 0     #Starting score
        self._weapon = ["bullet"]   #Weapons the ship is equipped with
        self._cur_weapon = "bullet" #default weapon
        self._bullets = pygame.sprite.Group()
        self._shield = pygame.sprite.Group()    #For orbs circulating the player
        self._speed = 3  #initial starting speed
        self._orb_count = 0
        self._time = 250
        self.sound = sound

    def right(self):
        """Moves the ship in the right direction, with the amount given by the self._speed"""
        if self.rect.x + self.width < self.screen.get_rect()[2]:
            self.rect.x += self._speed

    def left(self):
        """Moves the ship in the left direction"""
        if self.rect.x > 0:
            self.rect.x -= self._speed

    def get_topy(self):
        return self.rect.top

    def getx(self):
        """Return the x-coordinate of the center of ship"""
        return self.rect.centerx

    def gety(self):
        """Return the y-coordinate of the center of ship"""
        return self.rect.centery

    def shoot(self):
        """Adds a Bullet or Rocket to the bullets group"""
        if self._cur_weapon == "bullet" and self._ammo["bullet"] > 0:
            self.sound.play_destroy("bullet")
            self._bullets.add(Bullet(self.rect.x+self.width/2, self.rect.y + self.height, 3))
            self._ammo["bullet"] -= 1
        elif self._cur_weapon == "rocket" and self._ammo["rocket"] > 0:
            self.sound.play_destroy("rocket")
            self._bullets.add(Rocket(self.rect.x+self.width/2, self.rect.y, 3))
            self._ammo["rocket"] -= 1
        elif self._cur_weapon == "dual" and self._ammo["bullet"] > 0:
            self.sound.play_destroy("bullet")
            self._bullets.add(Bullet(self.rect.x+self.width/2 - 4, self.rect.y + self.height, 3))
            self._bullets.add(Bullet(self.rect.x+self.width/2 + 4, self.rect.y + self.height, 3))
            self._ammo["bullet"] -= 2
        elif self._cur_weapon == "spread" and self._ammo["spread"] > 0:
            self.sound.play_destroy("spread")
            self._bullets.add(DotWeapon(self.rect.x+self.width/2, self.rect.y + self.height, 10))
            self._bullets.add(AngleBullet(self.rect.x+self.width/2, self.rect.y + self.height, 3, 1))
            self._bullets.add(AngleBullet(self.rect.x+self.width/2, self.rect.y + self.height, 3, -1))



            #self._bullets.add(AngleBullet(self.rect.x+self.width/2, self.rect.y + self.height, 3, 0))
            self._ammo["spread"] -= 3

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
        else:
            self._health = 100

    def get_ammo(self):
        """Returns the amount of ammo remaining"""
        if self._cur_weapon == "dual":
            return self._ammo["bullet"]
        else:
            return self._ammo[self._cur_weapon]

    def get_ammolimit(self):
        """Returns the ammo limit for the equipped weapon"""
        if self._cur_weapon == "dual":
            return self._ammo_limits["bullet"]
        else:
            return self._ammo_limits[self._cur_weapon]

    def add_ammo(self, weapon, amount):
        """Increments the player's ammunition"""
        if self._ammo[weapon] + amount < self._ammo_limits[weapon]:
            self._ammo[weapon] += amount
        else:
            self._ammo[weapon] = self._ammo_limits[weapon]

    def decrement_ammo(self, amount, weapon):
        self._ammo[weapon] -= amount

    def update_score(self, amount):
        """updates the score of the ship, 10 per-kill"""
        self._score += amount

    def get_score(self):
        """Returns the score"""
        return self._score

    def get_bullets(self):
        """Returns the group containing the bullets"""
        return self._bullets

    def update(self):
        """Updates bullets and shield, and draws them on screen"""
        self._bullets.update()
        self._bullets.draw(self.screen)
        if self._orb_count > 0:
            self._time -= 0.05
            self._shield.update(self._time)
            self._shield.draw(self.screen)

    def add_weapon(self, weapon):
        """appends a weapon to the weapon's list if it is not already in there"""
        if weapon not in self._weapon:
            self._weapon.append(weapon)

    def get_weapon(self):
        """Returns the weapon currently equipped"""
        return self._cur_weapon

    def get_all_weapons(self):
        """Returns all the weapons available for use"""
        return self._weapon

    def change_weapon(self):
        """Reshuffles the weapons' list, putting the first weapon at the back of list
        and setting the current weapon to be the first element in the list
        """
        if len(self._weapon) != 1:
            self._weapon.append(self._weapon.pop(0))
            self._cur_weapon = self._weapon[0]

    def set_weapon(self, weapon):
        """Sets the weapon to be immediately equiped"""
        self._cur_weapon = weapon

    def get_speed(self):
        """Returns the current speed of ship"""
        return self._speed

    def add_speed(self):
        """Increments the speed by 1 provided self._speed < 10  """
        if self._speed < 10:
            self._speed += 1

    def add_orb(self):
        """Adds an additional orb to circulate the ship"""
        if self._orb_count < 6:
            self._orb_count += 1
            self._orb_reset()

    def delete_orb(self):
        """Deletes an orb"""
        self._orb_count -= 1
        if self._orb_count != 0:
            self._orb_reset()

    def _orb_reset(self):
        """Clears the shield group and resets the positions of the orbs"""
        self._shield.empty()
        angle = 2*math.pi/self._orb_count
        for n in range(self._orb_count):
            self._shield.add(Orb(self, n*angle))

    def get_shield(self):
        """Returns the group containing the orbs which circulate the ship"""
        return self._shield

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = self._draw_bullet()
        self.rect = self.image.get_rect()
        self.rect.y = y - 12
        self.rect.x = x-self.rect.width/2
        self.speed = speed
        #self.play_sound()

    def play_sound(self):
        """Plays the sound"""
        pygame.mixer.Sound("Laser.wav").play()

    def _draw_bullet(self):
        """Draws the bullet shape onto the surface. Returns the surface"""
        image = pygame.Surface([2, 12])
        image.fill(colour.RED)
        return image

    def update(self):
        """Updates position of bullet i.e. moves it up the screen. If it moves off the screen it is automatically destroyed"""
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

    def get_amount(self):
        """Returns the amount of damage this weapon will do"""
        return 5


    def __str__(self):
        return "bullet"

class DotWeapon(Bullet):
    """Dot weapon, used for spread weapon"""
    def _draw_bullet(self):
        return sprites.dotbullet()

    def play_sound(self):
        pygame.mixer.Sound("sounds/Laser_Shoot.wav").play()

    def get_amount (self):
        return 2

    def __str__(self):
        return "default"



class AngleBullet(Bullet):
    def __init__(self, x, y, speed, dir):
        Bullet.__init__(self, x, y, speed)
        self.vector = vector.Vector(dir, 5)
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def _draw_bullet(self ):
        """Draws the bullet shape onto the surface and returns it"""
        #image = pygame.Surface([2, 12], pygame.SRCALPHA)
        #pygame.draw.rect(image, colour.RED, (0, 0, 2, 12))

        return sprites.dotbullet()

    def update(self):
        """Updates the position of the bullet. ie. moves it across and up the screen
        destroys the bullet if exceed screen height
        """
        self.rect.x += self.vector.getx() * 2
        self.rect.y -= self.vector.gety() * 2
        if self.rect.y < 0:
            self.kill()

    def get_amount(self):
        return 2

    def __str__(self):
        return "spread"

class Rocket(Bullet):
    def _draw_bullet(self):
        return sprites.rocket()

    def __str__(self):
        return "rocket"

class BulletDown(Bullet):
    """Class BulletUp inherits from Bullet. The method 'update' has been modified to move the bullet down"""

    def __init__(self, x, y, speed):
        Bullet.__init__(self, x, y, speed)
        self.image = self._draw_bullet()
        self._amount = 0

    def _draw_bullet(self):
        """Draws the bullet shape onto the surface. Returns the surface"""
        image = pygame.Surface([2, 12])
        image.fill(colour.CYAN)
        return image

    def update(self):
        """Updates position of bullet, i.e. moves it down. If it moves off the screen it is automatically destroyed"""
        self.rect.y += self.speed
        if self.rect.y > self.screen.get_rect()[3]:
            self.kill()

    def get_amount(self):
        self._amount = 20
        return self._amount

class HealthPack(BulletDown):
    """Class HealthPack inherits from BulletDown"""
    def _draw_bullet(self):
        """Draws a health pack"""
        return sprites.healthpack()

    def __str__(self):
        return "health"

    def get_amount(self):
        self._amount = random.randint(5, 10)
        return self._amount

    def get_text1(self):
        """Returns the text to be displayed on obtaining this object
        Precondition self.get_amount() has been called prior
        """
        return "+" + str(self._amount)

class RocketDrop(BulletDown):
    def _draw_bullet(self):
        """Draws the rocket drop"""
        return sprites.rocketdrop()

    def __str__(self):
        return "rocketitem"

    def get_amount(self):
        self._amount = 3
        return self._amount

    def get_text1(self):
        return "Rocket Launcher Obtained"

    def get_text2(self):
        return "+" + str(self._amount)


class AmmoPack(BulletDown):
    """Class AmmoPack inherits from BulletDown"""
    def _draw_bullet(self):
        return sprites.ammopack()

    def __str__(self):
        return "ammo"

    def get_amount(self):
        """Returns a random amount of ammo"""
        self._amount = random.randint(5, 15)
        return self._amount

    def get_text1(self):
        return "+" + str(self._amount)


class SpeedBoost(BulletDown):
    def _draw_bullet(self):
        return sprites.speedboost()

    def __str__(self):
        return "speed"

    def get_amount(self):
        """Return the boost in speed value"""
        self._amount = 1
        return self._amount

    def get_text1(self):
        return "+" + str(self._amount) + " speed"

class DualBullet(BulletDown):
    def _draw_bullet(self):
        """Draws the dual bullet drop"""
        return sprites.dual_bullet()

    def __str__(self):
        return "dual"

    def get_amount(self):
        self._amount = 15
        return self._amount

    def get_text1(self):
        return "Dual Rail Gun Attachment Obtained"

    def get_text2(self):
        return "+" + str(self._amount)

class SpreadBullet(BulletDown):
    def _draw_bullet(self):
        """draws the spread bullet drop"""
        return sprites.spread_icon()

    def __str__(self):
        return "spread"

    def get_amount(self):
        self._amount = 30
        return self._amount

    def get_text1(self):
        return "Wide Shot Canon Obtained"

    def get_text2(self):
        return "+" + str(self._amount)

class ShieldItem(BulletDown):
    def _draw_bullet(self):
        """draws the spread bullet drop"""
        return sprites.shield_drop()

    def __str__(self):
        return "orb"

    def get_text1(self):
        """Returns the text to display when item is shield drop is obtained"""
        return "1+ Shield"

class EnemyCluster(object):
    """ This class groups together enemy ships, it is automatically populated"""
    def __init__(self, draw_screen, sound):
        self.screen = pygame.display.get_surface()
        self.enemies = pygame.sprite.Group()
        self.health_bars = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self._enemieslst = []
        self.total = 0
        self.count = 0 #No. of enemy ships at any given time
        self._populate()
        self.screen = draw_screen
        self.center = self.screen.get_rect()[2]/2
        self.old_time = time.clock()
        self.sound = sound
        self.speed = 1
        self.diry = 0 # 1=down 0=no vertical movement
        self.dirx = self.speed # 1=right, -1=left


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
        for row, y in enumerate(range(int(0.1*height),height/2, 40)):
            self._enemieslst.append([])
            for col, x in enumerate(range(int(left), int(right), 80)):
                temp = Enemy(x, y, 30, 30, self, (row, col))
                self._enemieslst[-1].append(temp)
                self.health_bars.add(interface.HealthBar(temp, x, y, 30, 4))
                self.enemies.add(temp)
                self.count += 1
        self.total = self.count

    def _shoot(self):
        """Randomly selects a ship from the group and calls its shoot method"""
        if time.clock() - self.old_time > 0.25 * self.speed:
            #print "Selecting random ship"
            select = random.randint(0, len(self.enemies.sprites())-1)
            self.sound.play_destroy("enemy_shoot", 0.02)
            self.bullets.add(self.enemies.sprites()[select].shoot())
            self.old_time = time.clock()

    def _move_ships(self):
        """Updates the ship's position"""
        for ship in self.enemies.sprites():
            ship.move(self.dirx, self.diry)
        #print self.direction
        self.diry = 0

    def _move_health(self):
        """Moves the heathbars, call this to update their position after enemy ships have moved"""
        for h in self.health_bars:
            h.move()

    def update(self):
        if self.dirx > 0:
            if self.center > 0.60*self.screen.get_rect()[2]:
                self.dirx = -self.speed
                self.diry = 5
        else:
            if self.center < 0.40*self.screen.get_rect()[2]:
                self.dirx = self.speed
                self.diry = 5

        self.center += self.dirx
        self._move_ships()
        self._move_health()
        self.enemies.draw(self.screen)
        self.health_bars.draw(self.screen)
        self.bullets.update()
        self.bullets.draw(self.screen)
        self.items.update()
        self.items.draw(self.screen)
        self._shoot()

    def getRowCol(self):
        """Return number of rows and cols of enemy ships"""
        return len(self._enemieslst), len(self._enemieslst[-1])

    def destroySelected(self, row, col, amount):
        """Destroys a selected enemy (if it hasn't already been destroyed) in the list given the row and col
        Precondition row, col must be valid index
        """

        if self._enemieslst[row][col].get_health() > 0 and self._enemieslst[row][col].destroy(amount):
            self.count -= 1
            self.sound.play_destroy("enemy")
            if self.count < 0.1*self.total:
                self.speed = 4
            elif self.count < 0.2*self.total:
                self.speed = 3
            elif self.count < 0.5*self.total:
                self.speed = 2
            return True
        else:
            return False

    def ships_remaining(self):
        """Return the no. of ships remaining"""
        return self.count


class Enemy(pygame.sprite.Sprite):
    """This class represents the enemy sprites"""
    def __init__(self, x, y, width, height, parent, pos):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = self._draw_sprite()
        #pygame.draw.rect(self.image, colour.BLUE, (0,0,width,height))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.width = width
        self.height = height
        self.health = 10
        self.parent = parent
        self.pos = pos    #Position in list in terms for row and column

    def _draw_sprite(self):
        col = colour.PURPLE
        image = pygame.Surface([30, 25], pygame.SRCALPHA)
        pygame.draw.rect(image, col, (5, 0, 20, 20))
        pygame.draw.rect(image, colour.BLACK, (7, 5, 4, 4))
        pygame.draw.rect(image, colour.BLACK, (19, 5, 4, 4))
        pygame.draw.rect(image, colour.BLACK, (10, 13, 10, 4))
        pygame.draw.rect(image, col, (0, 15, 5, 15))
        pygame.draw.rect(image, col, (25, 15, 5, 10))
        return image

    def destroy(self, amount):
        """Plays the destruction sound of the enemy ship, returns true if enemy is destroyed"""
        self.health -= amount
        if self.health <= 0:
            self.kill()
            ran = random.randint(1, 12)
            if ran == 1:
                self.parent.items.add(HealthPack(self.rect.x, self.rect.y, 2))
            elif ran == 2:
                self.parent.items.add(AmmoPack(self.rect.x, self.rect.y, 2))
            elif ran == 3:
                self.parent.items.add(DualBullet(self.rect.x, self.rect.y, 2))
            elif ran == 4:
                self.parent.items.add(RocketDrop(self.rect.x, self.rect.y, 2))
            elif ran == 5:
                self.parent.items.add(SpeedBoost(self.rect.x, self.rect.y, 2))
            elif ran == 6:
                self.parent.items.add(SpreadBullet(self.rect.x, self.rect.y, 2))
            elif ran == 7:
                self.parent.items.add(ShieldItem(self.rect.x, self.rect.y, 2))
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

    def get_pos(self):
        """Returns the position in terms of rows and cols in list"""
        return self.pos

class Orb(pygame.sprite.Sprite):
    def __init__(self, player, startangle):
        pygame.sprite.Sprite.__init__(self)
        self.image = self._draw_orb()
        self.rect = self.image.get_rect()
        self.angle = startangle
        self.player = player

    def _draw_orb(self):
        return sprites.orb()

    def update(self, time):
        self.rect.centerx = self.player.getx() + 30*math.cos(time+self.angle)
        self.rect.centery = self.player.gety() + 30*math.sin(time+self.angle)