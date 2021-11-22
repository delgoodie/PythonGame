from Game.Components.Sprite import Sprite
from Util.Vec2 import Vec2
import pygame
import os


class Collider:
    def __init__(self, type: str, pos: Vec2, arg, layer: int, parent=None):
        self.type = type
        self.pos = pos
        self.layer = layer
        self.parent = parent
        if type == "circle":
            self.radius = arg
            self.sprite = Sprite(pygame.image.load(os.path.join("Assets", "collision_circle.png")), self.pos, 0, Vec2(2, 2) * self.radius)
        elif type == "rect":
            self.size = arg
            self.sprite = Sprite(pygame.image.load(os.path.join("Assets", "collision_rect.png")), self.pos, 0, self.size, 1)

    @property
    def tr(self):
        return self.pos + self.size * Vec2(1, 1) * 0.5

    @property
    def tl(self):
        return self.pos + self.size * Vec2(-1, 1) * 0.5

    @property
    def br(self):
        return self.pos + self.size * Vec2(1, -1) * 0.5

    @property
    def bl(self):
        return self.pos + self.size * Vec2(-1, -1) * 0.5

    @property
    def top(self):
        return self.pos.y + self.size.y * 0.5

    @property
    def bottom(self):
        return self.pos.y - self.size.y * 0.5

    @property
    def right(self):
        return self.pos.x + self.size.x * 0.5

    @property
    def left(self):
        return self.pos.x - self.size.x * 0.5
