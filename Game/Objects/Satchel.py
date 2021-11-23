import math
import os
import pygame
from Game.Components.Collider import Collider
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite


class Satchel:
    def __init__(self, game):
        self.image = pygame.image.load(os.path.join("Assets", "satchel.png"))
        self.game = game
        self.items = [None, None, None, None, None]
        self.item_index = -1
        self.item_sprite = Sprite(self.image, Vec2(0, 0), 0, Vec2(0.35, 0.35), 2)

    def can_add_item(self):
        return self.item_index < 4

    def add_item(self, item):
        if self.can_add_item():
            self.item_index += 1
            self.items[self.item_index] = item

    def can_remove_item(self):
        return self.item_index > -1

    def remove_item(self):
        if self.can_remove_item():
            item = self.items[self.item_index]
            self.items[self.item_index] = None
            self.item_index -= 1
            return item

    def update(self, timestep: float):
        pass

    def item_render(self, pos: Vec2, angle: float, sprites: list[Sprite]):
        self.item_sprite.pos = pos
        self.item_sprite.angle = angle + 3 * math.pi / 4
        sprites.append(self.item_sprite)
