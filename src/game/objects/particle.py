import math
from os import times
from game.components.shapes import Rects, Sprite
from util.vec2 import Vec2
import random


class Particle:
    def __init__(
        self,
        pos: Vec2,
        game,
        time: int,
        dir=Vec2(1, 0),
        colors=[(255, 255, 255)],
        gain=math.pi / 2,
        lifetime=100,
        vel=1.0,
        acc=1.0,
        size=1.0,
        rate=2,
        disp=0,
    ):
        self.pos = pos
        self.game = game
        self.time = time

        self.dir = dir.normalized()
        self.colors = colors
        self.gain = gain
        self.lifetime = lifetime
        self.vel = vel
        self.acc = acc
        self.size = size
        self.rate = rate
        self.disp = disp

        self.num_particles = 0

        self.duration = 0

        self.particles = []

    def create_particle(self):
        angle_offset = 8 * (random.random() - 0.5) ** 3 * self.gain / 2
        dir = self.dir.copy()
        dir.t += angle_offset

        pos = self.pos.copy()
        if self.disp != 0:
            disp = Vec2(1, 0)
            disp.t += random.random() * math.pi * 2
            disp.r *= self.disp * random.random()
            pos += disp

        self.particles.append(
            {
                "pos": pos,
                "color": self.colors[random.randrange(0, len(self.colors))],
                "size": self.size,
                "vel": dir * self.vel,
                "duration": 0,
            }
        )

    def update(self, timestep):
        self.duration += timestep
        if self.duration > self.time and len(self.particles) == 0:
            self.game.remove_object(self)
            del self
            return

        num_new_particles = math.floor(self.rate * self.duration - self.num_particles) if self.duration < self.time else 0

        for i in range(num_new_particles):
            self.create_particle()

        self.num_particles += num_new_particles

        remove_indicies = []

        for index, particle in enumerate(self.particles):
            particle["pos"] += particle["vel"]
            particle["vel"] += particle["vel"] * self.acc
            particle["duration"] += timestep
            if particle["duration"] > self.lifetime:
                remove_indicies.append(index)

        for index in reversed(remove_indicies):
            self.particles.pop(index)

    def render(self, shapes: list[Sprite | Rects]):
        shapes.append(Rects([(p["color"], p["pos"], Vec2(p["size"], p["size"])) for p in self.particles], layer=4))
