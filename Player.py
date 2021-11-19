import pygame
from Vec2 import Vec2
from Sprite import Sprite
import os


guy_rect = pygame.Rect(100, 100, 440 / 4, 360 / 4)


class Player:
    def __init__(self, position: Vec2):
        self.p = position
        self.sprite = Sprite(os.path.join("Assets", "guy.png"), Vec2(440, 360), 0.25)

    def render(self, window: pygame.Surface):
        window.blit(self.sprite.render(self.p.x), self.p.tup)
