import pygame
import sys
from objects import Player,Obstacle,grid
from screen import screen_widht,screen_height

pygame.init()
screen = pygame.display.set_mode((screen_widht, screen_height))
pygame.display.set_caption('Space invaders')
pygame_icon = pygame.image.load('sprites/green.png')
pygame.display.set_icon(pygame_icon)

class Game():

    def __init__(self):

        self.player_sprite = Player((screen_widht/2,screen_height),screen_widht,5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.obstacles = self.create_obstacles()

    def create_obstacles(self):
        obtacles_width = len(grid[0]) * 3
        gap = (screen_widht -(obtacles_width*4))/5
        obstacles = []
        for o in range(4):
            set_x = (o + 1)* gap + o * obtacles_width
            obstacle = Obstacle(set_x, screen_height - 100)
            obstacles.append(obstacle)
        return obstacles

    def run(self):
        self.player.update()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        for self.obstacle in self.obstacles:
            self.obstacle.blocks_group.draw(screen)


game = Game()
clock = pygame.time.Clock()

while True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    game.run()
    pygame.display.flip()
    clock.tick(60)
