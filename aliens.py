import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self,spri,x,y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.type = spri
        self.path = f'resources/{spri}.png'
        self.image=pygame.image.load(self.path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.exploding = False
        self.explosion_time = 0
        if spri == 'green':
            self.explosion_image = pygame.image.load('resources/explosion_green.png').convert_alpha()
        elif spri == 'yellow':
            self.explosion_image = pygame.image.load('resources/explosion_yellow.png').convert_alpha()
        else:
            self.explosion_image = pygame.image.load('resources/explosion_red.png').convert_alpha()

    def explode(self):
        self.image = self.explosion_image
        self.exploding = True
        self.explosion_time = pygame.time.get_ticks()
    def update(self, direction):
        if not self.exploding:
            self.rect.x += direction
        else:
            self.rect.x += direction
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_time > 500:
                self.kill()

class MisteryShip(pygame.sprite.Sprite):
    def __init__(self,screen_width):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.scren_width = screen_width
        self.image = pygame.image.load('resources/mystery.png').convert_alpha()
        self.x = random.choice([0, self.scren_width - self.image.get_width()])
        self.exploding = False
        self.explosion_time = 0
        self.explosion_image = pygame.image.load('resources/mystery_explosion.png').convert_alpha()
        if self.x == 0:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft=(self.x,50))
    def explode(self):
        self.image = self.explosion_image
        self.exploding = True
        self.explosion_time = pygame.time.get_ticks()
    def update(self):
        if self.exploding:
            self.rect.x += self.speed
            if pygame.time.get_ticks() - self.explosion_time > 500:
                self.kill()
        else:
            self.rect.x += self.speed
            if self.rect.right > self.scren_width:
                self.kill()
            elif self.rect.left < 0:
                self.kill()