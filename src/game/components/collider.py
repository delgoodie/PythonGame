from game.components.shapes import Sprite
from util.vec2 import Vec2
import pygame
import os


class Collider:
    def __init__(self, pos: Vec2, size: Vec2, layer: int, parent=None):
        self.type = type
        self.pos = pos
        self.layer = layer
        self.parent = parent
        self.size = size

    # region Getters
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

    # endregion

    def point_inside(self, p: Vec2):
        return p.x >= self.left and p.x <= self.right and p.y >= self.bottom and p.y <= self.top

    def point_on_edge(self, p: Vec2):
        return (p.x >= self.left and p.x <= self.right and (p.y == self.top or p.y == self.bottom)) or (
            p.y >= self.bottom and p.y <= self.top and (p.x == self.left or p.x == self.right)
        )

    def ray_inteserction(self, o: Vec2, d: Vec2):

        # Edge Cases
        if d.x == 0 and d.y == 0:
            return None
        elif d.x == 0:
            if self.point_inside(o):
                return Vec2(o.x, self.top if d.y > 0 else self.bottom)
            else:
                if o.x >= self.left and o.x <= self.right:
                    if d.y > 0 and o.y <= self.bottom:
                        return Vec2(o.x, self.bottom)
                    elif d.y < 0 and o.y >= self.top:
                        return Vec2(o.x, self.top)
                return None
        elif d.y == 0:
            if self.point_inside(o):
                return Vec2(self.right if d.x > 0 else self.left, o.y)
            else:
                if o.x >= self.left and o.x <= self.right:
                    if d.x > 0 and o.y <= self.left:
                        return Vec2(self.left, o.y)
                    elif d.x < 0 and o.x >= self.right:
                        return Vec2(o.x, self.right, o.y)
                return None

        # d.x != 0 and d.y != 0
        m = d.y / d.x
        b = o.y - m * o.x

        ints: list[Vec2] = []
        l_y = m * self.left + b
        if l_y >= self.bottom and l_y <= self.top:
            ints.append(Vec2(self.left, l_y))

        r_y = m * self.right + b
        if r_y >= self.bottom and r_y <= self.top:
            ints.append(Vec2(self.right, r_y))

        b_x = (self.bottom - b) / m
        if b_x >= self.left and b_x <= self.right:
            ints.append(Vec2(b_x, self.bottom))

        t_x = (self.top - b) / m
        if t_x >= self.left and t_x <= self.right:
            ints.append(Vec2(t_x, self.top))

        closestInt = None
        for p in ints:
            if closestInt is None or (o - p).sqrMag < (o - closestInt).sqrMag:
                closestInt = p

        return closestInt
