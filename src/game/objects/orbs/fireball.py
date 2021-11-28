import math
import os
import pygame
from game.components.animation import Animation, Animator
from game.components.collider import Collider
from game.objects.particle import Particle
from util.vec2 import Vec2
from game.components.shapes import Rects, Sprite


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

    def update(self, timestep: int):
        if len(self.game.physics.find_cols(self.collider, [1])) > 0:
            self.game.remove_object(self)
            self.game.add_object(
                Particle(
                    self.pos + self.dir * 0.15,
                    self.game,
                    120,
                    dir=-self.dir,
                    size=0.075,
                    vel=0.04,
                    acc=0,
                    colors=[(255, 161, 0), (223, 131, 38)],
                    lifetime=90,
                    rate=0.3,
                    disp=0.075,
                    gain=1,
                )
            )
            del self
            return
        self.pos += self.dir * self.speed * (timestep / 1000)

    def render(self, shapes: list[Sprite | Rects]):
        shapes.append(Sprite(self.animator.get_image(), self.pos, self.dir.t + 3 * math.pi / 2, Vec2(0.5, 0.5), 5))
        if self.game.debug > 2:
            shapes.append(self.collider.sprite)
