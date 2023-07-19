import pygame

from random import randint

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.birds import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManeger:
   
    def __init__(self):
        self.obstacles = []
        self.alternate_append_index = 0

    def update(self, game):
        if len(self.obstacles) == 0:
            self.alternate_append_index = randint(0, 2)
            if self.alternate_append_index == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif self.alternate_append_index == 1:
                self.obstacles.append(Bird(BIRD))
            else:
                self.obstacles.append(Cactus(LARGE_CACTUS))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                game.playing = False
                break

    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacles(self):
        self.obstacles= []