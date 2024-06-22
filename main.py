import pygame
import sys
import random
from objects import Player, Obstacle, grid, Alien, Laser,MisteryShip
from screen import screen_widht, screen_height

pygame.init()
screen = pygame.display.set_mode((screen_widht, screen_height))
pygame.display.set_caption('Space Invaders')
pygame_icon = pygame.image.load('resources/green.png')
pygame.display.set_icon(pygame_icon)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER,500)
MISTERY_SHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MISTERY_SHIP,random.randint(20000,40000))

class Game:
    def __init__(self):
        self.player_sprite = Player((screen_widht / 2, screen_height), screen_widht, 5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.lasers_aliens = pygame.sprite.Group()
        self.misteryship = pygame.sprite.GroupSingle()
        self.lives = 3
        self.running = True

    def create_obstacles(self):
        obtacles_width = len(grid[0]) * 3
        gap = (screen_widht - (obtacles_width * 4)) / 5
        obstacles = []
        for o in range(4):
            set_x = (o + 1) * gap + o * obtacles_width
            obstacle = Obstacle(set_x, screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55
                if row == 0:
                    alien_sprite = 'green'
                elif row in (1, 2):
                    alien_sprite = 'yellow'
                else:
                    alien_sprite = 'red'
                self.alien = Alien(alien_sprite, x, y)
                self.aliens_group.add(self.alien)

    def create_misteryship(self):
        self.misteryship.add(MisteryShip(screen_widht))

    def move_aliens(self):
        for alien in self.aliens_group:
            alien.update(self.aliens_direction)
        self.alien_sprites = self.aliens_group
        for alien in self.alien_sprites:
            if alien.rect.right >= screen_widht:
                self.aliens_direction = -1
                self.aliens_move_down(2)
            elif alien.rect.left <= 0:
                self.aliens_direction = 1
                self.aliens_move_down(2)

    def aliens_move_down(self, direction):
        if self.alien_sprites:
            for alien in self.alien_sprites:
                alien.rect.y += direction

    def aliens_shoot_laser(self):
        if self.aliens_group.sprites():
            self.random_alien = random.choice(self.aliens_group.sprites())
            self.alien_laser = Laser((self.random_alien.rect.center), speed=-5)
            self.lasers_aliens.add(self.alien_laser)

    def check_for_collisions(self):
        if self.player_sprite.lasers:
            for laser in self.player_sprite.lasers:
                collided_aliens = pygame.sprite.spritecollide(laser, self.aliens_group, False)
                if collided_aliens:
                    for alien in collided_aliens:
                        alien.explode()
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.misteryship,True):
                    laser.kill()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser,obstacle.blocks_group,True):
                        laser.kill()
        if self.lasers_aliens:
            for laser in self.lasers_aliens:
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()
                if pygame.sprite.spritecollide(laser,self.player_sprite.lasers,True):
                    laser.kill()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser,obstacle.blocks_group,True):
                        laser.kill()
        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien,obstacle.blocks_group,True)
                if pygame.sprite.spritecollide(alien,self.player,False):
                    self.game_over()

    def game_over(self):
        self.running = False

    def reset(self):
        self.running = True
        self.lives = 3
        self.player_sprite.reset()
        self.aliens_group.empty()
        self.lasers_aliens.empty()
        self.create_aliens()
        self.misteryship.empty()
        self.obstacles = self.create_obstacles()

    def run(self):

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        for self.obstacle in self.obstacles:
            self.obstacle.blocks_group.draw(screen)
        self.aliens_group.draw(screen)
        self.lasers_aliens.draw(screen)
        self.misteryship.draw(screen)
        self.check_for_collisions()
        if self.running == True:
            self.misteryship.update()
            self.lasers_aliens.update()
            self.player.update()
            self.move_aliens()
game = Game()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.running== True:
            game.aliens_shoot_laser()
        if event.type == MISTERY_SHIP and game.running== True:
            game.create_misteryship()
            pygame.time.set_timer(MISTERY_SHIP,random.randint(20000,40000))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and game.running == False:
            game.reset()

    screen.fill((0, 0, 0))
    game.run()
    pygame.display.flip()
    clock.tick(60)
