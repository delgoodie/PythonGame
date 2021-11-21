import pygame
from Application import Application
from Camera import Camera
from Player import Player
from Vec2 import Vec2
from World import World


class Game:
    def __init__(self):
        self.player = Player(Vec2(0, 0))
        self.map = 0
        self.camera = Camera(Vec2(2, 0), 10)
        self.world = World("path")

    def handle_input(self, input):
        dir = Vec2(0, 0)
        if input["a"]:
            dir.x -= 1
        if input["d"]:
            dir.x += 1
        if input["w"]:
            dir.y += 1
        if input["s"]:
            dir.y -= 1

        if dir.r > 1:
            dir.r = 1

        scroll = int(input["left"]) - int(input["right"])
        action1 = input["up"]
        action2 = input["down"]
        boost = input["space"]
        strafe = input["shift"]
        pickup = input["e"]

        self.player.move(dir, scroll, action1, action2, boost, strafe, pickup)

    def update(self, timestep: float):
        self.camera.pos = self.player.pos.copy()
        self.player.update(timestep)

    def render(self, window: pygame.Surface):
        sprites = []
        self.world.render(sprites)
        self.player.render(sprites)
        # self.map.render(sprites)

        self.camera.draw(window, sprites)

    def hud_render(self, window):
        self.player.hud_render(window)

    def loop(self, app: Application):
        self.handle_input(app.input)

        self.update(app.timestep)

        # self.camera.pos.t += app.timestep

        self.render(app.window)

        self.hud_render(app.window)
