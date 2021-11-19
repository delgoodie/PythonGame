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

        # rot_rect = rot_image.get_rect(center=rect.center)
        # return rot_image,rot_rect

        if not rotation is None:
            angle = rotation - self._rotation
            rotated_surface = pygame.transform.rotate(self._surface, angle)
            # new_rect = rotated_surface.get_rect(center=self._surface.get_rect().center)
            # self._rotation = rotation
            self._surface = rotated_surface
            # self._position.tup = (new_rect[0], new_rect[1])

        if not scale is None:
            if type(scale) is float:
                scale = Vec2(scale, scale)
            scale_change = scale / self._scale
            self._surface = pygame.transform.scale(self._surface, scale_change.tup)
            self._scale = scale

        return self._surface
