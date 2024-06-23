import pygame
from laser import Laser
from screen import screen_height,screen_widht

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,constraint,speed):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('resources/player.png').convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(midbottom=(pos))
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.cooldown = 600
        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('resources/Sounds_laser.ogg')
        self.laser_sound.set_volume(0.2)
        self.playerhit = pygame.image.load('resources/playerhit.png').convert_alpha()
        self.hit = False
        self.hit_time = 0
        self.hit_duration = 1000
        self.blink_interval = 100

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def contraints(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def recharge(self):
        if self.ready == False:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.laser_time >= self.cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,))

    def reset(self):
        self.rect = self.image.get_rect(midbottom=(screen_widht/2, screen_height))
        self.lasers.empty()
    def got_hit(self):
        self.image = self.playerhit
        self.hit = True
        self.hit_time = pygame.time.get_ticks()
        self.blink_start_time = self.hit_time

    def update(self):
        self.get_input()
        self.contraints()
        self.recharge()
        self.lasers.update()
        if self.hit:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.hit_time
            if elapsed_time < self.hit_duration:
                if (current_time - self.blink_start_time) // self.blink_interval % 2 == 0:
                    self.image = self.playerhit
                else:
                    self.image = self.original_image
            else:
                self.image = self.original_image
                self.hit = False