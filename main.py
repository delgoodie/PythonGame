import pygame
import os
from app import Application

GUY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "guy.png")), (440 / 4, 360 / 4))

guy_rect = pygame.Rect(100, 100, 440 / 4, 360 / 4)


def loop(input, window, app_status):
    if input["a"]:
        guy_rect.x -= 3
    if input["d"]:
        guy_rect.x += 3
    if input["w"]:
        guy_rect.y -= 3
    if input["s"]:
        guy_rect.y += 3

    window.fill((255, 255, 0))
    window.blit(GUY, guy_rect)


def main():
    Application(loop)


if __name__ == "__main__":
    main()
