import math
import os
import pygame
from game.components.collider import Collider
from util.vec2 import Vec2
from game.components.sprite import Sprite


class Satchel:
    def __init__(self, game):
        self.image = pygame.image.load(os.path.join("Assets", "satchel.png"))
        self.game = game
        self.items = [None, None, None, None, None]
        self.item_index = -1
        self.hand_sprite = Sprite(self.image, Vec2(0, 0), 0, Vec2(0.35, 0.35), 2)

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

    def hand_render(self, pos: Vec2, angle: float, sprites: list[Sprite]):
        self.hand_sprite.pos = pos
        self.hand_sprite.angle = angle + 3 * math.pi / 4
        sprites.append(self.hand_sprite)

    def item_render(self, pos: Vec2, window: pygame.Surface):
        width = window.get_width()
        length = 3 * width / (13 * 4)

        item_image = pygame.transform.scale(self.image, (length, length))

        window.blit(item_image, item_image.get_rect(center=pos.tup))
