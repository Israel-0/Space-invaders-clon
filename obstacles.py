import pygame

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

class Block(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,3))
        self.image.fill('paleturquoise1')
        self.rect = self.image.get_rect(topleft = pos)
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