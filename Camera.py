import math
import pygame
from pygame import transform
from Sprite import Sprite
from Vec2 import Vec2


class Camera:
    def __init__(self, pos: Vec2, diagonal: float):
        self.pos = pos
        self.diagonal = diagonal
        self.debug = True

    def transform_length(self, length: float):
        screen_diagonal = math.hypot(*pygame.display.get_window_size())
        return (screen_diagonal / self.diagonal) * length

    def transform_point(self, point: Vec2) -> Vec2:
        screen_size = Vec2(*pygame.display.get_window_size())

        relative_point = point - self.pos  # game vector from cam (center of screen) to point

        pixel_point = Vec2(self.transform_length(relative_point.x), self.transform_length(relative_point.y))

        pixel_point = pixel_point * Vec2(1, -1) + screen_size / 2  # account for (0, 0) in top right, not center

        return pixel_point

    def transform_image(self, sprite: Sprite):
        image = sprite.image.copy()

        rect = image.get_rect(center=self.transform_point(sprite.pos).tup)

        pixel_size = Vec2(self.transform_length(sprite.size.x), self.transform_length(sprite.size.y))

        image = pygame.transform.scale(image, pixel_size.tup)

        image = pygame.transform.rotate(image, math.degrees(sprite.angle))

        rect = image.get_rect(center=rect.center)

        return image, rect

    def draw(self, window: pygame.Surface, sprites: list[Sprite]):
        images = [self.transform_image(sprite) for sprite in sprites]
        window.blits(images)

        if self.debug:
            for image in images:
                pygame.draw.circle(window, (255, 0, 0), image[1].center, 5)
                pygame.draw.rect(window, (255, 0, 0), image[1], 2)
