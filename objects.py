import pygame
from screen import screen_height

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,constraint,speed):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(pos))
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.cooldown = 600
        self.lasers = pygame.sprite.Group()

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

    def update(self):
        self.get_input()
        self.contraints()
        self.recharge()
        self.lasers.update()


class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed = 5):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4,20))
        self.image.fill('White')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= screen_height + 50:
            self.kill()

    def update(self):
        self.rect.y -= self.speed
        self.destroy()


class Block(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,3))
        self.image.fill('White')
        self.rect = self.image.get_rect(topleft = pos)

grid = [
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
]

class Obstacle():
    def __init__(self,x,y):
        self.blocks_group = pygame.sprite.Group()
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 1:
                    pos_x = x + column * 3
                    pos_y = y + row * 3
                    block = Block((pos_x,pos_y))
                    self.blocks_group.add(block)