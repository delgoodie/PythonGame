import math
import os
import pygame
from game.components.button_handler import ButtonHandler
from game.components.collider import Collider
from game.objects.ingredients.berry import Berry
from game.objects.orbs.fireball import Fireball
from util.vec2 import Vec2
from game.components.shapes import Rects, Sprite


class FireCrystal:
    def __init__(self, pos: Vec2, game):
        self.pos = pos
        self.image = pygame.image.load(os.path.join("Assets", "fire_crystal.png"))
        self.sprite = Sprite(self.image, self.pos, 0, Vec2(0.4, 0.4), 5)
        self.hand_sprite = Sprite(self.image, self.pos, 0, Vec2(0.4, 0.4), 2)

        self.game = game
        self.collider = Collider(self.pos, Vec2(0.4, 0.4), 4, self)

        self.invoke_handler = ButtonHandler(300)

        self.crafts = {(Berry,): FireCrystal}

    def invoke(self, value, player, pos: Vec2, dir: Vec2):
        self.invoke_handler.update(value)
        if self.invoke_handler.value:
            self.game.add_object(Fireball(pos, dir, player, self.game))

    def try_craft(self, ingredients):
        ing_types_set = set([type(ing) for ing in ingredients])
        for key in self.crafts:
            if set(key) == ing_types_set:
                return self.crafts[key]
        return None

    def update(self, timestep: int):
        pass

    def render(self, shapes: list[Sprite | Rects]):
        shapes.append(self.sprite)

    def hand_render(self, pos: Vec2, angle: float, sprites: list[Sprite]):
        self.hand_sprite.pos = pos
        self.hand_sprite.angle = pygame.time.get_ticks() / 180
        sprites.append(self.hand_sprite)

    def item_render(self, pos: Vec2, window: pygame.Surface):
        width = window.get_width()
        length = 3 * width / (13 * 4)

        item_image = pygame.transform.scale(self.image, (length, length))

        window.blit(item_image, item_image.get_rect(center=pos.tup))
