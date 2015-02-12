import interface
import colour
import game_objects
import pygame
import time
import random
import textmsg

__author__ = 'justin'



class Game(object):
    """Class which handles the entire game"""
    def __init__(self, screen, sound, col):
        """Precondition: pygame must be initialized prior to creating a Game instance"""
        self.screen = screen
        self._clock = pygame.time.Clock()
        self.sound = sound
        self._width = self.screen.get_width()
        self._height = self.screen.get_height()
        self._player_sprite = pygame.sprite.Group()
        self._health_sprite = pygame.sprite.Group()
        self._init_interface()
        self._player_sprite.add(self._player)
        self._player_bullets = pygame.sprite.Group()
        self._enemy_cluster = game_objects.EnemyCluster(self, 1, col)
        self._status = True
        self._text = []
        self._stars = [[random.randrange(0, self._width-1), random.randrange(0, self._height-1),
                       random.randrange(1, 4)] for _ in range(256)]
        self._bg_update()
        self._new_level(1)

    def _init_interface(self):
        health = interface.HealthBar2(self._width*0.75, self._height*0.02, 175, 18)
        ammo = interface.AmmoBar(self._width*0.50, self._height*0.02, 175, 18)
        equip = interface.Equip(self._width*0.30, self._height*0.02)
        self._score = interface.Score(self._width*0.07, self._height*0.02)
        self._player = game_objects.Ship(self, health, ammo, equip)
        self._statusTop = interface.TopStatusBar(health, ammo, equip, self._score)

    def _bg_update(self):
        """Redraws the background, run this prior to drawing game objects"""
        self.screen.fill(colour.BLACK)
        for star in self._stars:
            if star[2] + star[1] > self._height:
                star[1] = 0
            else:
                star[1] += star[2]
            self.screen.set_at((star[0], star[1]), colour.WHITE)

    def _text_update(self):
        """Updates all scrolling Text and removes them if necessary"""
        for t in self._text:
            if t.distance_travel() > 70:
                del t
            else:
                t.move_y(-1)

    def _new_level(self, lvl):
        """displaye new level text ie. level 1"""
        save_s = self.screen.copy()
        text = interface.TextCenter(self._width/2, self._height/2, 30, colour.GREEN)
        oldtime = time.clock()
        while True:
            if time.clock() > oldtime + 0.5:
                break
            else:
                self.screen.blit(save_s, (0, 0))
                text.render("Level " + str(lvl))
                pygame.display.update()

    def win(self):
        """Move to the next level, resets the enemycluster"""
        lvl = self._enemy_cluster.new_level()
        self._enemy_cluster.reset()
        self._player.reset()
        self._new_level(lvl)

    def lose(self):
        """Displays Gameover msg, run when player loses"""
        paused = True
        save_s = self.screen.copy()
        gameover_text = interface.TextCenter(self._width/2, self._height/2, 30, colour.GREEN)
        key_text = interface.TextCenter(self._width/2, self._height/2 + 40, 30, colour.GREEN)
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self._status = False
                    paused = False
                    break
            self.screen.blit(save_s, (0, 0))
            gameover_text.render("GAME OVER")
            key_text.render("Press Enter to Continue")
            pygame.display.update()


    def _pause(self):
        """Pauses the game (freeze game state) until player presses p"""
        paused = True
        save_s = self.screen.copy()
        pause_text = interface.TextCenter(self._width/2, self._height/2 - 40, 30, colour.GREEN)
        cont_text = interface.TextCenter(self._width/2, self._height/2, 30, colour.GREEN)
        quit_text = interface.TextCenter(self._width/2, self._height/2 + 40, 30, colour.GREEN)
        oldtime = 0
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                        break
                    elif event.key == pygame.K_q:
                        paused = False
                        self._status = False
                        break
                if event.type == pygame.QUIT:
                    raise SystemExit
            if time.clock() - oldtime > 0.1:
                self.screen.blit(save_s, (0, 0))
            if time.clock() - oldtime > 0.2:
                pause_text.render("Game Paused")
                cont_text.render("Press P to continue playing")
                quit_text.render("Press Q to Quit to Main Menu")
                oldtime = time.clock()
            pygame.display.update()

    def _collision(self):
        """Checks for collisions and take appropriate action if necessary"""
        collide_player = pygame.sprite.groupcollide(self._enemy_cluster.get_ships(), self._player.get_bullets(), False, True)
        collide_enemy = pygame.sprite.spritecollide(self._player, self._enemy_cluster.get_bullets(), True)
        collide_item = pygame.sprite.spritecollide(self._player, self._enemy_cluster.get_items(), True)
        collide_enemyplayer = pygame.sprite.spritecollide(self._player, self._enemy_cluster.get_ships(), False)
        collide_shield = pygame.sprite.groupcollide(self._player.get_shield(), self._enemy_cluster.get_bullets(), True, True)

        if collide_player != {}:    #When bullet collides with enemy ship
            for enemy in collide_player.iterkeys():
                row, col = enemy.get_pos()
                for bullet in collide_player[enemy]:
                    damage = bullet.get_amount()
                    if self._enemy_cluster.destroySelected(row, col, damage):
                        self._score.update_score(10)
                    if str(bullet) == "rocket":
                        row, col = enemy.get_pos()
                        count = 0
                        if col > 0: #destroy left side
                            if self._enemy_cluster.destroySelected(row, col-1, damage):
                                count += 1
                        if col < self._enemy_cluster.getRowCol()[1]-1:
                            if self._enemy_cluster.destroySelected(row, col+1, damage):
                                count += 1
                        if row > 0:
                            if self._enemy_cluster.destroySelected(row-1, col, damage):
                                count += 1
                        if row < self._enemy_cluster.getRowCol()[0]-1:
                            if self._enemy_cluster.destroySelected(row+1, col, damage):
                                count += 1
                        self._score.update_score(count*5)

        if collide_enemy:   #When enemy bullet collides with player
            for bullet in collide_enemy:
                amount = bullet.get_amount()
                amount = bullet.get_amount()
                self._score.update_score(-5)
                self._player.take_damage(amount)
                self._text.append(interface.ScrollText(self._player.getx(), self._player.gety(),
                                                          20, "-" + str(amount), colour.RED))
                if self._player.get_health() < 15:
                    self._text.append(interface.ScrollText(self._player.getx() + 70, self._player.gety(),
                                                          20, "Health Critical", colour.RED))
                if self._player.get_health() < 25:
                    self._text.append(interface.ScrollText(self._player.getx() + 70, self._player.gety(),
                                                          20, "Health Low", colour.RED))

        if collide_item:    #When item collides with player 
            for item in collide_item:
                amount = item.get_amount()
                if str(item) == "health":
                    self.sound.play_powerup("health")
                    self._player.add_health(amount)
                    self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.increase(amount), colour.GREEN))
                elif str(item) == "ammo":
                    self.sound.play_powerup("ammo")
                    if self._player.add_ammo('bullet', amount):
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.increase(amount), colour.J_GREEN))
                    else:
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.Max.ammo, colour.J_GREEN))

                elif str(item) == "rocketitem":
                    if "rocket" not in self._player.get_all_weapons():
                        self.sound.play_powerup("weapon")
                        self._player.add_weapon("rocket")
                        self._player.set_weapon("rocket")
                        #self._statusTop.new_equip()
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                        20, textmsg.NewWeapon.rocket, colour.GREY))
                    else:
                        self.sound.play_powerup("ammo")
                        if self._player.add_ammo("rocket", amount):
                            self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                        20, textmsg.increase(amount), colour.GREY))
                        else:
                            self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                        20, textmsg.Max.rocket, colour.GREY))

                elif str(item) == "dual":
                    if "dual" not in self._player.get_all_weapons():
                        self.sound.play_powerup("weapon")
                        self._player.add_weapon("dual")
                        self._player.set_weapon("dual")
                        #self._statusTop.new_equip()
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.NewWeapon.dual, colour.RED))

                    else:
                        self.sound.play_powerup("ammo")
                        if self._player.add_ammo("bullet", 20):
                            self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.increase(amount), colour.J_GREEN))
                        else:
                            self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.Max.ammo, colour.J_GREEN))

                elif str(item) == "spread":
                    if "spread" not in self._player.get_all_weapons():
                        self.sound.play_powerup("weapon")
                        self._player.add_weapon("spread")
                        self._player.set_weapon("spread")
                        #self._statusTop.new_equip()
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.NewWeapon.spread, colour.BLUE))
                    else:
                        self.sound.play_powerup("ammo")
                        if self._player.add_ammo("spread", amount):
                            self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.increase(amount), colour.BLUE))
                        else:
                            self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.Max.ammo, colour.BLUE))

                elif str(item) == "speed":
                    self.sound.play_powerup("speed")
                    if self._player.add_speed():
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.increase(amount) + " speed", colour.YELLOW))
                    else:
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.Max.speed, colour.YELLOW))


                elif str(item) == "orb":
                    self.sound.play_powerup("shield")
                    if self._player.add_orb():
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.increase(amount) + " shield", colour.WHITE))
                    else:
                        self._text.append(interface.ScrollText(self._player.getx(), self._player.get_topy(),
                                                          20, textmsg.Max.shield, colour.WHITE))
        if collide_enemyplayer:         #Enemy ship collides with the player ship
            self._player.take_damage(100)

        if collide_shield:
            self._player.delete_orb()

    def run(self):
        while self._status:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self._player.left()
            elif keys[pygame.K_RIGHT]:
                self._player.right()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #and len(self._player_bullets.sprites())<6:
                        self._player.shoot()
                    elif event.key == pygame.K_p:
                        self._pause()
                    elif event.key == pygame.K_x:
                        self._player.change_weapon()
                    elif event.key == pygame.K_c:
                        self._player.eject_orb()
            self._bg_update()
            self._text_update()
            self._player_sprite.draw(self.screen)
            self._statusTop.update()
            self._collision()
            self._player_sprite.update()
            self._enemy_cluster.update()
            self._clock.tick(80)
            pygame.display.update()
        return 0