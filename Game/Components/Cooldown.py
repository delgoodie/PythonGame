import pygame


class Cooldown:
    def __init__(self, time):
        self.time = time
        self.start_time = 0

    def within(self, t):
        return self.time - self.get_timer() <= t

    def get_timer(self):
        return self.time - float(pygame.time.get_ticks()) / 1000 + self.start_time

    def ready(self):
        if self.get_timer() <= 0:
            self.start_time = float(pygame.time.get_ticks()) / 1000
            return True
        return False
