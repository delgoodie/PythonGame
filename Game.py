import pygame
from Player import Player
from Vec2 import Vec2


class Game:
    def __init__(self):
        self.player = Player(Vec2(0, 0))

    def loop(self, input, window: pygame.Surface, app_status):
        if input["a"]:
            self.player.position.x -= 1
        if input["d"]:
            self.player.position.x += 3
        if input["w"]:
            self.player.position.y -= 3
        if input["s"]:
            self.player.position.y += 3

        window.fill((255, 255, 0))
        self.player.render(window)
