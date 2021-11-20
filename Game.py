import pygame
from Player import Player
from Vec2 import Vec2


class Game:
    def __init__(self):
        self.player = Player(Vec2(0, 0))

    def handle_input(self, input):
        direction = Vec2(0, 0)
        if input["a"]:
            direction.x -= 1
        if input["d"]:
            direction.x += 1
        if input["w"]:
            direction.y -= 1
        if input["s"]:
            direction.y += 1
        self.player.move(direction, 0, False, False, False, False)

    def update(self):
        self.player.update()

    def render(self, window: pygame.Surface):
        window.fill((255, 255, 255))
        self.player.render(window)

    def hud_render(self, window):
        pass

    def loop(self, input, window: pygame.Surface, app_status):

        self.handle_input(input)

        self.update()

        self.render(window)

        self.hud_render(window)
