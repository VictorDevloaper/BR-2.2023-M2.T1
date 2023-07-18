from random import randint

from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.type = randint(0, 1)
        super().__init__(image, self.type, False)
        self.rect.y = randint(260, 310)