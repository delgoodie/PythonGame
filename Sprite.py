import pygame
from Vec2 import Vec2


class Sprite:
    def __init__(self, image: pygame.Surface, pos:Vec2, angle:float, size:Vec2):
        self.image = image
        self.pos = pos
        self.angle = angle
        self.size = size