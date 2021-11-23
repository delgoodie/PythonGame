import math
import os
import pygame
from Game.Components.Collider import Collider
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite


class Fireball:
    def __init__(self, pos: Vec2, dir: Vec2, player, game):
        self.pos = pos
        self.dir = dir
        self.speed = 4
        self.image = pygame.image.load(os.path.join("Assets", "fireball.png"))
        self.sprite = Sprite(self.image, self.pos, self.dir.t + math.pi / 2, Vec2(0.4, 0.4), 5)

        self.game = game
        self.collider = Collider("rect", self.pos, Vec2(0.4, 0.4), 4, self)

    def update(self, timestep: float):
        self.pos += self.dir * self.speed * timestep

    def render(self, sprites: list[Sprite]):
        sprites.append(self.sprite)
