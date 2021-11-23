import math
import os
import pygame
from Game.Components.Collider import Collider
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite


class Berry:
    def __init__(self, pos: Vec2, game):
        self.pos = pos
        self.image = pygame.image.load(os.path.join("Assets", "berry.png"))
        self.sprite = Sprite(self.image, self.pos, 0, Vec2(0.4, 0.4), 5)
        self.hand_sprite = Sprite(self.image, self.pos, 0, Vec2(0.3, 0.3), 2)

        self.game = game
        self.collider = Collider("rect", self.pos, Vec2(0.4, 0.4), 4, self)

    def update(self, timestep: float):
        pass

    def render(self, sprites: list[Sprite]):
        sprites.append(self.sprite)
        if self.game.debug > 2:
            sprites.append(self.collider.sprite)

    def hand_render(self, pos: Vec2, angle: float, sprites: list[Sprite]):
        self.hand_sprite.pos = pos
        self.hand_sprite.angle = angle + 3 * math.pi / 2
        sprites.append(self.hand_sprite)

    def item_render(self, pos: Vec2, window: pygame.Surface):
        width = window.get_width()
        length = 3 * width / (13 * 4)

        item_image = pygame.transform.scale(self.image, (length, length))

        window.blit(item_image, item_image.get_rect(center=pos.tup))
