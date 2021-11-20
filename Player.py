import pygame
from Vec2 import Vec2
from Sprite import Sprite
import os
import math


class Player:
    def __init__(self, position: Vec2):
        self.position = position
        self.velocity = Vec2(0, 0)
        self.direction = Vec2(1, 0)
        self.sprite = Sprite(os.path.join("Assets", "player.png"), Vec2(440, 440), 0.25)

    def move(self, direction: Vec2, scroll: int, action1: bool, action2: bool, boost: bool, strafe: bool):
        self.velocity = direction
        if direction.r > 0 and not strafe:
            self.direction = direction

        # print(self.velocity)

    def update(self):
        self.position += self.velocity

    def render(self, window: pygame.Surface):
        # print(math.degrees(self.direction.t))
        image, rect = self.sprite.render(self.position, math.degrees(self.direction.t))
        print(math.degrees(self.direction.t))
        window.blit(image, rect)
