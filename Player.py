import pygame
from Vec2 import Vec2
from Sprite import Sprite
import os


class Player:
    def __init__(self, pos: Vec2):
        self.pos = pos
        self.vel = Vec2(0, 0)
        self.acc = Vec2(0, 0)
        self.input_vel = Vec2(0, 0)
        self.dir = Vec2(1, 0)
        self.image = pygame.image.load(os.path.join("Assets", "player.png"))

    def move(self, dir: Vec2, scroll: int, action1: bool, action2: bool, boost: bool, strafe: bool, pickup: bool):
        self.input_vel = dir * (self.input_vel.r + 0.2)
        if dir.r > 0 and not strafe:
            self.dir = dir

    def update(self, timestep: float):
        self.acc += -self.vel * 0.05
        self.vel += self.acc * timestep
        self.pos += self.vel * timestep

        if self.input_vel.r > 2:
            self.input_vel.r = 2

        self.pos += self.input_vel * timestep

    def render(self, sprites: list[Sprite]):
        sprites.append(Sprite(self.image, self.pos, self.dir.t, Vec2(1, 1)))

    def hud_render(self, window: pygame.Surface):
        pass
