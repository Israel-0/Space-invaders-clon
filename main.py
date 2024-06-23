import pygame
import sys
import random
import csv
from player import Player
from laser import Laser
from aliens import Alien, MisteryShip
from obstacles import Obstacle, grid
from screen import screen_widht, screen_height

pygame.init()
screen = pygame.display.set_mode((screen_widht, screen_height))
pygame.display.set_caption('Space Invaders')
pygame_icon = pygame.image.load('resources/green.png')
pygame.display.set_icon(pygame_icon)
font = pygame.font.Font('resources/monogram.ttf', 30)
white = (255, 255, 255)

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
        self.aliens_speed = 1
        self.aliens_direction = 1
        self.lasers_aliens = pygame.sprite.Group()
        self.misteryship = pygame.sprite.GroupSingle()
        self.lives = 3
        self.running = True
        self.round = 1
        self.score = 0
        self.highscore = self.read_highscore()
        self.interface_height = 40
        self.explosion_sound = pygame.mixer.Sound('resources/Sounds_explosion.ogg')
        self.explosion_sound.set_volume(0.1)
        pygame.mixer.music.load('resources/Sounds_music.ogg')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer_music.play(-1)

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
            alien.update(self.aliens_direction * self.aliens_speed)
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
                if laser.rect.top < self.interface_height:
                    laser.kill()
                if collided_aliens:
                    for alien in collided_aliens:
                        alien.explode()
                        self.explosion_sound.play()
                        if alien.type == 'green':
                            self.score += 30
                        elif alien.type == 'yellow':
                            self.score += 20
                        else:
                            self.score += 10
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.misteryship,False):
                    self.score += 100
                    self.misteryship.sprite.explode()
                    self.explosion_sound.play()
                    laser.kill()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser,obstacle.blocks_group,True):
                        laser.kill()
        if self.lasers_aliens:
            for laser in self.lasers_aliens:
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    self.player_sprite.got_hit()
                    if self.lives == 0:
                        self.game_over()
                if pygame.sprite.spritecollide(laser,self.player_sprite.lasers,True):
                    self.explosion_sound.play()
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
        if self.score > self.highscore:
            self.highscore = self.score
            self.write_highscore()

    def reset(self):
        self.running = True
        self.lives = 3
        self.round = 1
        self.aliens_speed = 1
        self.score = 0
        self.player_sprite.reset()
        self.aliens_group.empty()
        self.lasers_aliens.empty()
        self.create_aliens()
        self.misteryship.empty()
        self.obstacles = self.create_obstacles()
    def round_up(self):
        if self.running == True and len(self.aliens_group) == 0 and len(self.misteryship) == 0:
            self.player_sprite.reset()
            self.lasers_aliens.empty()
            self.round += 1
            self.create_aliens()
            self.aliens_speed += 0.2

    def draw_interface(self):
        score_text = font.render(f'Score: {self.score}', True, white)
        highscore_text = font.render(f'Highscore: {self.highscore}', True, white)
        lives_text = font.render(f'Lives: {self.lives}', True, white)
        round_text = font.render(f'Round: {self.round}', True, white)
        game_over = font.render(f'You got {self.score} points in {self.round} rounds (Press ENTER to play again)', True, white)

        if self.running == True:
            screen.blit(score_text, (10, 10))
            screen.blit(highscore_text, ((screen_widht/2) -200, 10))
            screen.blit(lives_text, (screen_widht - 100, 10))
            screen.blit(round_text, (screen_widht - 220, 10))
        else:
            game_over_rect = game_over.get_rect(center=(screen_widht / 2, self.interface_height / 2))
            screen.blit(game_over, game_over_rect.topleft)

        pygame.draw.line(screen, white, (0, self.interface_height), (screen_widht, self.interface_height), 2)
    def read_highscore(self):
        try:
            with open('highscore.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    return int(row[0])
        except FileNotFoundError:
            return 0

    def write_highscore(self):
        with open('highscore.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.highscore])

    def run(self):

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        for self.obstacle in self.obstacles:
            self.obstacle.blocks_group.draw(screen)
        self.aliens_group.draw(screen)
        self.lasers_aliens.draw(screen)
        self.misteryship.draw(screen)
        self.check_for_collisions()
        self.draw_interface()
        if self.running == True:
            self.round_up()
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
