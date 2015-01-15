__author__ = 'justin'
import pygame
import game_objects
import interface
import time
import random
import colour
import textmsg

WIDTH = 1024
HEIGHT = 720

class Main(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.player_sprite = pygame.sprite.Group()
        self.health_sprite = pygame.sprite.Group()
        self.player = game_objects.Ship()
        self.player_sprite.add(self.player)
        self.player_bullets = pygame.sprite.Group()
        self.enemy_cluster = game_objects.EnemyCluster(self.screen)
        self.statusTop = interface.TopStatusBar(self.player)
        self.statusBot = interface.BotStatusBar()
        #star locations for bg
        self.stars = [[random.randrange(0,WIDTH-1), random.randrange(0,HEIGHT-1),
                       random.randrange(1,4)] for _ in range(256)]

    def bg_update(self):
        """Redraws the background, run this prior to drawing game objects"""
        self.screen.fill(colour.BLACK)
        for star in self.stars:
            if star[2] + star[1] > HEIGHT:
                star[1] = 0
            else:
                star[1] += star[2]

            self.screen.set_at((star[0], star[1]), colour.WHITE)

    def _pause(self):
        """Pauses the game (freeze game state) until player presses p"""
        paused = True
        save_s = self.screen.copy()
        pause_text = interface.Text(WIDTH/2, HEIGHT/2, 30)
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
            collide_player = pygame.sprite.groupcollide(self.enemy_cluster.get_ships(), self.player.get_bullets(), False, True)
            collide_enemy = pygame.sprite.spritecollide(self.player, self.enemy_cluster.get_bullets(), True)
            collide_item = pygame.sprite.spritecollide(self.player, self.enemy_cluster.get_items(), True)

            if collide_player != {}:
                for enemy in collide_player.iterkeys():
                    row, col = enemy.get_pos()
                    for bullet in collide_player[enemy]:
                        if self.enemy_cluster.destroySelected(row, col, 5):
                            self.player.update_score(10)
                        if str(bullet) == "rocket":
                            row, col = enemy.get_pos()
                            count=0
                            if col > 0: #destroy left side
                                if self.enemy_cluster.destroySelected(row, col-1, 5):
                                    count+=1
                            if col < self.enemy_cluster.getRowCol()[1]-1:
                                if self.enemy_cluster.destroySelected(row, col+1, 5):
                                    count+=1
                            if row > 0:
                                if self.enemy_cluster.destroySelected(row-1, col, 5):
                                    count+=1
                            if row < self.enemy_cluster.getRowCol()[0]-1:
                                if self.enemy_cluster.destroySelected(row+1, col, 5):
                                    count+=1
                            self.player.update_score(count*5)

            if collide_enemy:
                self.player.take_damage(10)

            if collide_item:
                for item in collide_item:
                    if str(item) == "health":
                        amount = item.get_amount()
                        self.player.add_health(amount)
                        self.statusBot.display(textmsg.non_weapon(str(item), amount))
                    elif str(item) == "ammo":
                        amount = item.get_amount()
                        self.player.add_ammo(amount)
                        self.statusBot.display(textmsg.non_weapon(str(item), amount))
                    elif str(item) == "rocketitem":
                        self.statusBot.display(textmsg.msg[str(item)])
                        self.player.add_weapon("rocket")
                    elif str(item) == "dual":
                        self.statusBot.display(textmsg.msg[str(item)])
                        self.player.add_weapon("dual")


    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.left(5)
            elif keys[pygame.K_RIGHT]:
                self.player.right(5)
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
            self.bg_update()
            self.player_sprite.draw(self.screen)
            self.player_sprite.update()
            self.enemy_cluster.update()
            self.statusTop.update()
            self.statusBot.update()
            self._collision()

            self.clock.tick(80)
            pygame.display.update()

if __name__ == "__main__":
    app = Main()
    app.run()