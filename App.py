import pygame
import os
from Input import Input

WIDTH, HEIGHT = 900, 500

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

INPUT = Input()

APP_STATUS = True

FPS = 60


def event_handler():
    global INPUT, APP_STATUS
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            APP_STATUS = False
    INPUT.read(events)


def Application(loop):
    pygame.display.set_caption("GAME")
    clock = pygame.time.Clock()

    while APP_STATUS:
        clock.tick(FPS)

        WINDOW.fill((255, 255, 0))

        event_handler()

        loop(INPUT, WINDOW, APP_STATUS)

        pygame.display.update()

    pygame.quit()
