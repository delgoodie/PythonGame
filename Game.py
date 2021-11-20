import pygame
from Application import Application
from Camera import Camera
from Player import Player
from Vec2 import Vec2


class Game:
    def __init__(self):
        self.player = Player(Vec2(0, 0))
        self.map = 0
        self.camera = Camera(Vec2(2, 0), 10)

    def handle_input(self, input):
        direction = Vec2(0, 0)
        if input["a"]:
            direction.x -= 1
        if input["d"]:
            direction.x += 1
        if input["w"]:
            direction.y += 1
        if input["s"]:
            direction.y -= 1
        self.player.move(direction, 0, False, False, False, False)

    def update(self):
        self.player.update()

    def render(self, window: pygame.Surface):
        sprites = []

        self.player.render(sprites)
        # self.map.render(sprites)

        self.camera.draw(window, sprites)

    def hud_render(self, window):
        self.player.hud_render(window)

    def loop(self, app: Application):
        self.handle_input(app.input)

        self.update()

        # self.camera.pos.t += app.timestep

        self.render(app.window)

        self.hud_render(app.window)
