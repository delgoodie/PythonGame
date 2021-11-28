import pygame
from game.components.collider import Collider
from util.vec2 import Vec2
import os
from game.components.shapes import Rects, Sprite


class Map:
    def __init__(self, map_path, game):
        self.map = self.load_map(map_path)
        self.game = game

        self.floor_tile = pygame.image.load(os.path.join("Assets", "floor_tile.png"))
        self.wall_tile = pygame.image.load(os.path.join("Assets", "wall_tile.png"))
        self.collider_map = []
        for y in range(len(self.map)):
            self.collider_map.append([])
            for x in range(len(self.map[y])):
                if self.map[y][x]:
                    self.collider_map[y].append(Collider(Vec2(x, y), Vec2(1, 1), 1))
                    self.game.physics.colliders.append(self.collider_map[y][x])
                else:
                    self.collider_map[y].append(None)

    def load_map(self, map_path):
        return [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1],
        ]

    def render(self, shapes: list[Sprite | Rects]):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                shapes.append(Sprite(self.wall_tile if self.map[y][x] else self.floor_tile, Vec2(x, y), 0, Vec2(1.01, 1.01), 10))
