import pygame
from Vec2 import Vec2
from Sprite import Sprite
import os


class Player:
    def __init__(self, position: Vec2):
        self.position = position
        self.velocity = Vec2(0, 0)
        self.sprite = Sprite(os.path.join("Assets", "guy.png"), Vec2(440, 360), 0.25)

    def render(self, window: pygame.Surface):
        window.blit(self.sprite.render(self.position, self.position.x * 3.1 / 180), self.position.tup)
