import pygame
import os
from App import Application
from Player import Player
from Vec2 import Vec2

player = Player(Vec2(100, 100))


def loop(input, window: pygame.Surface, app_status):
    global player
    if input["a"]:
        player.p.x -= 1
    if input["d"]:
        player.p.x += 3
    if input["w"]:
        player.p.y -= 3
    if input["s"]:
        player.p.y += 3

    window.fill((255, 255, 0))
    player.render(window)


def main():
    Application(loop)


if __name__ == "__main__":
    main()
