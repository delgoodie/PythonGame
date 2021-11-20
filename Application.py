import pygame
import os
from Input import Input
import csv


class Application:
    def __init__(self, settings_path):
        self._settings_path = settings_path
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("GAME")
        self.input = Input()
        self.app_status = True
        self.fps = 60

        self._read_settings()

    def _read_settings(self):
        with open(self._settings_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            print("Reading ", self._settings_path)
            for row in reader:
                print(", ".join(row))

    def event_handler(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.app_status = False
        self.input.read(events)

    def run(self, loop):
        clock = pygame.time.Clock()

        while self.app_status:
            clock.tick(self.fps)

            self.event_handler()

            # TODO: or pass in self and give game full access to Application?
            loop(self.input, self.window, self.app_status)

            pygame.display.flip()

        pygame.quit()
