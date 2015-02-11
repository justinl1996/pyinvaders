import pygame
from data import interface, game_objects

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
    
player_sprite = pygame.sprite.Group()
health_sprite = pygame.sprite.Group()

player = game_objects.Ship(50, 10)
player_sprite.add(player)
player_bullets = pygame.sprite.Group()
enemy_cluster = game_objects.EnemyCluster(screen)
status = interface.StatusBar(player)


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.left(5)
    elif keys[pygame.K_RIGHT]:
        player.right(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(player_bullets.sprites())<6:
                player_bullets.add(player.shoot())

    screen.fill((255,255,255))
    player_sprite.draw(screen)
    player_bullets.update()
    player_bullets.draw(screen)
    enemy_cluster.update()
    collide_player = pygame.sprite.groupcollide(enemy_cluster.get_ships(), player_bullets, False, True)
    collide_enemy = pygame.sprite.spritecollide(player, enemy_cluster.get_bullets(), True)
    status.update()

    if collide_player != {}:
        for enemy in collide_player.iterkeys():
            if enemy.destroy():
                player.update_score(10)

    if collide_enemy:
        player.take_damage(10)

    clock.tick(60)
    pygame.display.update()
