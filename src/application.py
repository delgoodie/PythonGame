import pygame
from util.input import Input
import csv


class Application:
    def __init__(self, settings_path):
        self._settings_path = settings_path

        settings = self._read_settings()
        self.width = int(settings["width"]) or 500
        self.height = int(settings["height"]) or 900
        self.fps = int(settings["fps"]) or 60

        self.input = Input()
        self.app_status = True
        self.time = 0
        self.timestep = 0

        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("GAME")
        pygame.font.init()

    def _read_settings(self):
        csvfile = open(self._settings_path, newline="")
        csv_reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        settings_array = [row[0].split(",") for row in csv_reader]
        for setting in settings_array:
            if not type(setting) is list or len(setting) != 2:
                raise Exception("error in settings.csv")

        return dict(settings_array)

    def event_handler(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.app_status = False
        self.input.read(events)

    def run(self, loop):
        clock = pygame.time.Clock()

        while self.app_status:
            self.timestep = clock.tick(self.fps)
            self.time = pygame.time.get_ticks()

            self.window.fill((255, 255, 255))

            self.event_handler()

            loop(self)

            pygame.display.flip()

        pygame.quit()
