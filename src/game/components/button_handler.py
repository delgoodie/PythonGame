import pygame


class ButtonHandler:
    def __init__(self, cooldown: int):
        self.raw_value = False
        self.last_raw_value = False
        self.value = False

        self.start_pressed = self.start_released = pygame.time.get_ticks()
        self.duration_pressed = 0
        self.duration_released = 0

        self.start_cooldown = self.start_pressed
        self.cooldown = cooldown
        self.cooldown_duration = self.cooldown
        self.ready = False

    def update(self, value: bool):
        self.last_raw_value = self.raw_value
        self.raw_value = value

        ticks = pygame.time.get_ticks()

        # COOLED DOWN VALUE
        if not self.ready:
            self.cooldown_duration = ticks - self.start_cooldown
        self.ready = self.cooldown_duration > self.cooldown
        if self.ready and self.raw_value:
            self.value = True
            self.ready = False
            self.start_cooldown = ticks
        else:
            self.value = False

        # PRESSED & RELEASED Duration
        if not self.last_raw_value and self.value:
            self.start_pressed = ticks
        elif self.last_raw_value and not self.value:
            self.start_released = ticks
        elif self.raw_value:
            self.duration_pressed = ticks - self.start_pressed
        else:
            self.duration_pressed = ticks - self.start_pressed

        if self.raw_value and ticks - self.start_cooldown > self.cooldown:
            self.start_cooldown = ticks
