import pygame
from Vec2 import Vec2
import os
from Sprite import Sprite


class World:
    def __init__(self, map_path):
        self.map = self.load_map(map_path)
        self.floor_tile = pygame.image.load(os.path.join("Assets", "floor_tile.jpg"))
        self.wall_tile = pygame.image.load(os.path.join("Assets", "wall_tile.jpg"))

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

    def render(self, sprites: list[Sprite]):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                sprites.append(Sprite(self.wall_tile if self.map[y][x] else self.floor_tile, Vec2(x, y), 0, Vec2(1, 1)))
