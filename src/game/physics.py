from game.components.collider import Collider
from game.components.shapes import Rects, Sprite
from util.vec2 import Vec2
import pygame
import os


class Physics:
    def __init__(self, colliders: list[Collider]):
        self.colliders = colliders
        self.rect_collider_image = pygame.image.load(os.path.join("Assets", "collision_rect.png"))

    def find_cols(self, col: Collider, layers: list[int]):
        hits = []
        for other in self.colliders:
            if other.layer in layers and Physics.rect_rect(col, other):
                hits.append(other)

        return hits

    # region Legacy circle colliders
    # def circle_rect(circle: Collider, rect: Collider):
    #     closestPoint = Vec2(min(max(circle.pos.x, rect.left), rect.right), min(max(circle.pos.y, rect.bottom), rect.top))
    #     return (circle.pos - closestPoint).sqrMag < circle.radius ** 2

    # def circle_circle(circ1: Collider, circ2: Collider):
    #     return (circ1.pos - circ2.pos).sqrMag < (circ1.radius + circ2.radius) ** 2

    # def col_col(col_a: Collider, col_b: Collider) -> bool:
    #     if col_a.type == "rect":
    #         if col_b.type == "rect":
    #             return Physics.rect_rect(col_a, col_b)
    #         else:
    #             return Physics.circle_rect(col_b, col_a)
    #     else:
    #         if col_b.type == "rect":
    #             return Physics.circle_rect(col_a, col_b)
    #         else:
    #             return Physics.circle_circle(col_a, col_b)
    # endregion

    def rect_rect(rect1: Collider, rect2: Collider):
        return (
            rect1.point_inside(rect2.bl)
            or rect1.point_inside(rect2.tl)
            or rect1.point_inside(rect2.br)
            or rect1.point_inside(rect2.tr)
            or rect2.point_inside(rect1.bl)
            or rect2.point_inside(rect1.tl)
            or rect2.point_inside(rect1.br)
            or rect2.point_inside(rect1.tr)
        )

    def move(self, col: Collider, disp: Vec2, layers: list[int]):
        origin = col.pos.copy()

        col.pos += disp * Vec2(1, 0)

        for other in self.colliders:
            if other == col or not other.layer in layers:
                continue
            if Physics.rect_rect(col, other):
                col.pos.set(origin)

        origin2 = col.pos.copy()

        col.pos += disp * Vec2(0, 1)

        for other in self.colliders:
            if other == col or not other.layer in layers:
                continue
            if Physics.rect_rect(col, other):
                col.pos.set(origin2)
        return (col.pos - origin).r

    def render(self, shapes: list[Sprite | Rects]):
        for col in self.colliders:
            shapes.append(Sprite(self.rect_collider_image, col.pos, 0, col.size, 1))
