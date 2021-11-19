import pygame
from Vec2 import Vec2


class Sprite:
    def __init__(self, path: str, dimension: Vec2, rotation=0, scale=Vec2(1, 1)):
        self.path = path
        self._dimension = dimension
        self._rotation = rotation
        self._scale = Vec2(scale, scale) if type(scale) is float else scale

        self._surface = pygame.image.load(path)
        # pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), self._scale.tup), self._rotation)

    def render(self, rotation: float = None, scale: Vec2 = None):
        if not rotation is None:
            angle = rotation - self._rotation
            self._surface = pygame.transform.rotate(self._surface, angle)
            self._rotation = rotation
        if not scale is None:
            if type(scale) is float:
                scale = Vec2(scale, scale)
            scale_change = scale / self._scale
            self._surface = pygame.transform.scale(self._surface, scale_change.tup)
            self._scale = scale

        return self._surface
