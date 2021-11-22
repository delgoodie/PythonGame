import os
import pygame
from Game.Components.Collider import Collider
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite


class Berry:
    def __init__(self, pos: Vec2, game):
        self.pos = pos
        self.image = pygame.image.load(os.path.join("Assets", "berry.png"))
        self.sprite = Sprite(pygame.image.load(os.path.join("Assets", "berry.png")), self.pos, 0, Vec2(0.4, 0.4), 5)

        self.game = game
        self.collider = Collider("rect", self.pos, Vec2(0.4, 0.4), 4, self)

    def update(self, timestep: float):
        pass

    def render(self, sprites: list[Sprite]):
        sprites.append(self.sprite)
