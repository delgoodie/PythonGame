import pygame
from Vec2 import Vec2


class Sprite:
    def __init__(self, path: str, dimension: Vec2, position=Vec2(0, 0), rotation=0, scale=Vec2(1, 1)):
        self.path = path
        self._dimension = dimension
        self._position = position
        self._rotation = rotation
        self._scale = Vec2(scale, scale) if type(scale) is float else scale

        self._surface = pygame.image.load(path)
        # pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), self._scale.tup), self._rotation)

    def render(self, position: Vec2 = None, rotation: float = None, scale: Vec2 = None):
        if not position is None:
            self._position = position
        if not rotation is None:
            self._rotation = rotation
        if not scale is None:
            if type(scale) is float:
                self._scale = Vec2(scale, scale)
            elif type(scale) is Vec2:
                self._scale = scale

        image = self._surface.copy()

        rect = image.get_rect(center=self._position.tup)

        if self._scale != Vec2(1, 1):
            image = pygame.transform.scale(image, self._scale.tup)

        if self._rotation != 0:
            image = pygame.transform.rotate(image, 360 - self._rotation)
            rect = image.get_rect(center=self._surface.get_rect(center=self._position.tup).center)

        return image, rect
