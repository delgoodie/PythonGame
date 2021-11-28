import math
import pygame
from game.components.collider import Collider
from game.components.shapes import Rects, Sprite
from util.vec2 import Vec2


class Camera:
    def __init__(self, pos: Vec2, diagonal: float):
        self.pos = pos
        self.diagonal = diagonal
        self.debug = False
        # TODO: enable this at some point
        # pygame.mouse.set_visible(False)

    def transform_length(self, length: float):
        screen_diagonal = math.hypot(*pygame.display.get_window_size())
        return (screen_diagonal / self.diagonal) * length

    def transform_point(self, point: Vec2) -> Vec2:
        screen_size = Vec2(*pygame.display.get_window_size())

        relative_point = point - self.pos  # game vector from cam (center of screen) to point

        pixel_point = Vec2(self.transform_length(relative_point.x), self.transform_length(relative_point.y))

        pixel_point = pixel_point * Vec2(1, -1) + screen_size / 2  # account for (0, 0) in top right, not center

        pixel_point = Vec2(math.floor(pixel_point.x), math.floor(pixel_point.y))

        return pixel_point

    def transform_image(self, sprite: Sprite):
        image = sprite.image.copy()

        rect = image.get_rect(center=self.transform_point(sprite.pos).tup)

        pixel_size = Vec2(self.transform_length(sprite.size.x), self.transform_length(sprite.size.y))

        image = pygame.transform.scale(image, pixel_size.tup)

        image = pygame.transform.rotate(image, math.degrees(sprite.angle))

        rect = image.get_rect(center=rect.center)

        return image, rect

    def draw(self, window: pygame.Surface, shapes: list[Sprite | Rects]):
        def sort_func(shape: Sprite | Rects):
            return shape.layer

        shapes.sort(key=sort_func, reverse=True)

        images = []
        for shape in shapes:
            if type(shape) is Sprite:
                window.blit(*self.transform_image(shape))
            else:
                for rect in shape.rects:
                    pos = self.transform_point(rect[1])
                    size_x = self.transform_length(rect[2].x)
                    size_y = self.transform_length(rect[2].y)
                    pygame.draw.rect(window, rect[0], (pos.x, pos.y, size_x, size_y))

        if self.debug:
            for image in images:
                pygame.draw.circle(window, (255, 0, 0), image[1].center, 5)
                pygame.draw.rect(window, (255, 0, 0), image[1], 2)

    def draw_shadows(self, window: pygame.Surface, colliders: list[Collider]):
        polys = []
        for col in colliders:
            if col.layer == 1:
                pts = [col.tl, col.tr, col.br, col.bl]
                for i in range(len(pts)):
                    if Vec2.cross(self.pos - pts[i - 1], pts[i] - pts[i - 1]) > 0:
                        corners = [
                            pts[i],
                            pts[i] + (pts[i] - self.pos) * 1,
                            pts[i - 1] + (pts[i - 1] - self.pos) * 1,
                            pts[i - 1],
                        ]
                        polys.append([self.transform_point(p).tup for p in corners])
        for poly in polys:
            pygame.draw.polygon(window, (0, 0, 0), poly)
