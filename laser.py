import pygame
screen_height = 764

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