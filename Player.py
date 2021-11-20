import pygame
from Vec2 import Vec2
from Sprite import Sprite
import os


class Player:
    def __init__(self, pos: Vec2):
        self.pos = pos
        self.vel = Vec2(0, 0)
        self.dir = Vec2(1, 0)
        self.image = pygame.image.load(os.path.join("Assets", "player.png"))

    def move(self, direction: Vec2, scroll: int, action1: bool, action2: bool, boost: bool, strafe: bool):
        self.vel = direction * 0.05
        if direction.r > 0 and not strafe:
            self.dir = direction

    def update(self):
        self.pos += self.vel

    def render(self, sprites: list[Sprite]):
        sprites.append(Sprite(self.image, self.pos, self.dir.t, Vec2(1, 1)))

    def hud_render(self, window: pygame.Surface):
        pass
