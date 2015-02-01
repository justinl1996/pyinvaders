__author__ = 'justin'
import pygame
import game_objects
import interface
import time
import random
import colour

WIDTH = 1024
HEIGHT = 720

class Main(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.sound = interface.SoundEffects()
        self.player_sprite = pygame.sprite.Group()
        self.health_sprite = pygame.sprite.Group()
        self.player = game_objects.Ship(self.sound)
        self.player_sprite.add(self.player)
        self.player_bullets = pygame.sprite.Group()
        self.enemy_cluster = game_objects.EnemyCluster(self.screen, self.sound)
        self.statusTop = interface.TopStatusBar(self.player)
        #star locations for bg
        self.text = []

        self.stars = [[random.randrange(0, WIDTH-1), random.randrange(0,HEIGHT-1),
                       random.randrange(1, 4)] for _ in range(256)]

    def _bg_update(self):
        """Redraws the background, run this prior to drawing game objects"""
        self.screen.fill(colour.BLACK)
        for star in self.stars:
            if star[2] + star[1] > HEIGHT:
                star[1] = 0
            else:
                star[1] += star[2]
            self.screen.set_at((star[0], star[1]), colour.WHITE)

    def _text_update(self):
        """Updates all scrolling Text and removes them if necessary"""
        for t in self.text:
            if t.distance_travel() > 70 :
                del t
            else:
                t.move_y(-1)

    def _game_state(self):
        """checks to see if player has won -> return True. Otherwise return False"""
        if self.enemy_cluster.ships_remaining() == 0 or self.player.get_health() <= 0:
            return False
        else:
            return True


    def _pause(self):
        """Pauses the game (freeze game state) until player presses p"""
        paused = True
        save_s = self.screen.copy()
        pause_text = interface.TextCenter(WIDTH/2, HEIGHT/2, 30)
        oldtime = 0
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                if event.type == pygame.QUIT:
                    raise SystemExit

            if time.clock() - oldtime > 0.1:
                self.screen.blit(save_s, (0, 0))
            if time.clock() - oldtime > 0.2:
                pause_text.render("Game Paused, Press P to continue playing")
                oldtime = time.clock()

            pygame.display.update()

    def _collision(self):
        """Checks for collisions and take appropriate action if necessary"""
        collide_player = pygame.sprite.groupcollide(self.enemy_cluster.get_ships(), self.player.get_bullets(), False, True)
        collide_enemy = pygame.sprite.spritecollide(self.player, self.enemy_cluster.get_bullets(), True)
        collide_item = pygame.sprite.spritecollide(self.player, self.enemy_cluster.get_items(), True)
        collide_enemyplayer = pygame.sprite.spritecollide(self.player, self.enemy_cluster.get_ships(), False)
        collide_shield = pygame.sprite.groupcollide(self.player.get_shield(), self.enemy_cluster.get_bullets(), True, True)

        if collide_player != {}:    #When bullet collides with enemy ship
            for enemy in collide_player.iterkeys():
                row, col = enemy.get_pos()
                for bullet in collide_player[enemy]:
                    damage = bullet.get_amount()
                    if self.enemy_cluster.destroySelected(row, col, damage):
                        self.player.update_score(10)
                    if str(bullet) == "rocket":
                        row, col = enemy.get_pos()
                        count = 0
                        if col > 0: #destroy left side
                            if self.enemy_cluster.destroySelected(row, col-1, damage):
                                count += 1
                        if col < self.enemy_cluster.getRowCol()[1]-1:
                            if self.enemy_cluster.destroySelected(row, col+1, damage):
                                count += 1
                        if row > 0:
                            if self.enemy_cluster.destroySelected(row-1, col, damage):
                                count += 1
                        if row < self.enemy_cluster.getRowCol()[0]-1:
                            if self.enemy_cluster.destroySelected(row+1, col, damage):
                                count += 1
                        self.player.update_score(count*5)

        if collide_enemy:   #When enemy bullet collides with player
            for bullet in collide_enemy:
                amount = bullet.get_amount()
                amount = bullet.get_amount()
                self.player.update_score(-5)
                self.player.take_damage(amount)
                self.text.append(interface.ScrollText(self.player.getx(), self.player.gety(),
                                                          20, "-" + str(amount), colour.RED))
                if self.player.get_health() < 15:
                    self.text.append(interface.ScrollText(self.player.getx() + 70, self.player.gety(),
                                                          20, "Health Critical", colour.RED))
                if self.player.get_health() < 25:
                    self.text.append(interface.ScrollText(self.player.getx() + 70, self.player.gety(),
                                                          20, "Health Low", colour.RED))

        if collide_item:    #When item collides with player 
            for item in collide_item:
                amount = item.get_amount()
                if str(item) == "health":
                    self.sound.play_powerup("health")
                    self.player.add_health(amount)
                    self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text1(), colour.GREEN))
                elif str(item) == "ammo":
                    self.sound.play_powerup("ammo")
                    self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text1(), colour.J_GREEN))
                    self.player.add_ammo('bullet', amount)

                elif str(item) == "rocketitem":
                    if "rocket" not in self.player.get_all_weapons():
                        self.sound.play_powerup("weapon")
                        self.player.add_weapon("rocket")
                        self.player.set_weapon("rocket")
                        self.statusTop.new_equip()
                        self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                        20, item.get_text1(), colour.GREY))
                    else:
                        self.sound.play_powerup("ammo")
                        self.player.add_ammo("rocket", amount)
                        self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                        20, item.get_text2(), colour.GREY))
                elif str(item) == "dual":
                    if "dual" not in self.player.get_all_weapons():
                        self.sound.play_powerup("weapon")
                        self.player.add_weapon("dual")
                        self.player.set_weapon("dual")
                        self.statusTop.new_equip()
                        self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text1(), colour.RED))

                    else:
                        self.sound.play_powerup("ammo")
                        self.player.add_ammo("bullet", 20)
                        self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text2(), colour.J_GREEN))

                elif str(item) == "spread":
                    if "spread" not in self.player.get_all_weapons():
                        self.sound.play_powerup("weapon")
                        self.player.add_weapon("spread")
                        self.player.set_weapon("spread")
                        self.statusTop.new_equip()
                        self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text1(), colour.BLUE))
                    else:
                        self.sound.play_powerup("ammo")
                        self.player.add_ammo("spread", amount)
                        self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text2(), colour.BLUE))

                elif str(item) == "speed":
                    self.sound.play_powerup("speed")
                    self.player.add_speed()
                    self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text1(), colour.YELLOW))

                elif str(item) == "orb":
                    self.sound.play_powerup("shield")
                    self.player.add_orb()
                    self.text.append(interface.ScrollText(self.player.getx(), self.player.get_topy(),
                                                          20, item.get_text1(), colour.WHITE))
        if collide_enemyplayer:         #Enemy ship collides with the player ship
            self.player.take_damage(100)

        if collide_shield:
            self.player.delete_orb()

    def run(self):
        while self._game_state():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.left()
            elif keys[pygame.K_RIGHT]:
                self.player.right()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #and len(self.player_bullets.sprites())<6:
                        self.player.shoot()
                    elif event.key == pygame.K_p:
                        self._pause()
                    elif event.key == pygame.K_x:
                        self.player.change_weapon()
                        self.statusTop.new_equip()

            self._bg_update()
            self._text_update()
            self.player_sprite.draw(self.screen)
            self.player_sprite.update()
            self.enemy_cluster.update()
            self.statusTop.update()
            self._collision()
            self.clock.tick(80)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()