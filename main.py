import pygame
import ctypes

pygame.init()
user32 = ctypes.windll.user32

screen_widht= int(user32.GetSystemMetrics(0)/2)
screen_height= int(user32.GetSystemMetrics(1)-100)

screen = pygame.display.set_mode((screen_widht,screen_height))

clock = pygame.time.Clock()


spaceship_sprite=pygame.image.load('sprites/player.png').convert_alpha()
spaceship_rect = spaceship_sprite.get_rect(midbottom=(screen_widht / 2, screen_height - 10))
run = True
while run:
    clock.tick(60)

    screen.fill((0,0,0))

    screen.blit(spaceship_sprite,spaceship_rect)

    key = pygame.key.get_pressed()

    if key[pygame.K_d]:
        spaceship_rect.move_ip(5,0)
    elif key[pygame.K_a]:
        spaceship_rect.move_ip(-5,0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()