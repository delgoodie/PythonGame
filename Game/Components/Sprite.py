import pygame
from Util.Vec2 import Vec2


class Sprite:
    def __init__(self, image: pygame.Surface, pos: Vec2, angle: float, size: Vec2, layer=1):
        self.image = image
        self.pos = pos
        self.angle = angle
        self.size = size
        self.layer = layer
