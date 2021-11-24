import math
import os
import pygame
from Game.Components.Animation import Animation
from Game.Components.Animator import Animator
from game.components.collider import Collider
from util.vec2 import Vec2
from game.components.sprite import Sprite


class Fireball:
    def __init__(self, pos: Vec2, dir: Vec2, player, game):
        self.pos = pos
        self.dir = dir
        self.speed = 4

        self.animator = Animator(
            "fireball",
            [
                Animation(
                    "fireball",
                    Animation.images_from_spritesheet(pygame.image.load(os.path.join("Assets", "fireball.png")), 4),
                    [100, 100, 100, 100],
                    "fireball",
                    True,
                )
            ],
        )

        self.game = game
        self.collider = Collider("circle", self.pos, 0.15, 4, self)

    def update(self, timestep: float):
        if len(self.game.physics.find_cols(self.collider, [1])) > 0:
            self.game.remove_object(self)
            del self
            return
        self.pos += self.dir * self.speed * timestep

    def render(self, sprites: list[Sprite]):
        sprites.append(Sprite(self.animator.get_image(), self.pos, self.dir.t + 3 * math.pi / 2, Vec2(0.5, 0.5), 5))
        if self.game.debug > 2:
            sprites.append(self.collider.sprite)
