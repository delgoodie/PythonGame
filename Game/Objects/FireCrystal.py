import os
import pygame
from Game.Components.Collider import Collider
from Game.Components.Cooldown import Cooldown
from Game.Objects.Fireball import Fireball
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite


class FireCrystal:
    def __init__(self, pos: Vec2, game):
        self.pos = pos
        self.image = pygame.image.load(os.path.join("Assets", "fire_crystal.png"))
        self.sprite = Sprite(self.image, self.pos, 0, Vec2(0.4, 0.4), 5)
        self.item_sprite = Sprite(self.image, self.pos, 0, Vec2(0.3, 0.3), 2)

        self.game = game
        self.collider = Collider("rect", self.pos, Vec2(0.4, 0.4), 4, self)

        self.invoke_cooldown = Cooldown(0.3)

    def invoke(self, player, pos, dir):
        if self.invoke_cooldown.ready():
            self.game.add_object(Fireball(pos, dir, player, self.game))

    def update(self, timestep: float):
        pass

    def render(self, sprites: list[Sprite]):
        sprites.append(self.sprite)

    def item_render(self, pos: Vec2, angle: float, sprites: list[Sprite]):
        self.item_sprite.pos = pos
        self.item_sprite.angle = angle
        sprites.append(self.item_sprite)
