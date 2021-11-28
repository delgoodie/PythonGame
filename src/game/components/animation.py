import pygame


class Animation:
    def __init__(self, name: str, images: list[pygame.Surface], durations: list[int], next: str, cancelable: bool):
        self.name = name
        self._images = images
        self._durations = durations
        self.next = next
        self.cancelable = cancelable
        if len(images) != len(durations):
            raise Exception("number of images not equal to number of durations")

        self.duration = 0
        for d in durations:
            self.duration += d

    def get_image(self, cur_dur: int):
        for i in range(len(self._durations)):
            if cur_dur < self._durations[i]:
                return self._images[i]
            cur_dur -= self._durations[i]

    def images_from_spritesheet(spritesheet: pygame.Surface, length: int) -> list[pygame.Surface]:
        ss_width, ss_height = spritesheet.get_size()
        images = []
        for x in range(length):
            rect = pygame.Rect(x * (ss_width / length), 0, ss_width / length, ss_height)
            image = pygame.Surface(rect.size).convert()
            image.blit(spritesheet, (0, 0), rect)
            image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
            images.append(image)
        return images


class Animator:
    def __init__(self, initial_state_name: str, animations: list[Animation]):
        self.state_name = initial_state_name
        self.start_time = pygame.time.get_ticks()
        self.animations = dict([(anim.name, anim) for anim in animations])

    @property
    def state(self) -> Animation:
        if not self.state_name is None:
            return self.animations[self.state_name]
        return None

    def get_image(self):
        while True:
            if self.state_name is None:
                return None
            cur_dur = pygame.time.get_ticks() - self.start_time
            if cur_dur < self.state.duration:
                return self.state.get_image(cur_dur)
            else:
                self.start_time += self.state.duration
                self.state_name = self.state.next

    def try_change_state(self, new_state_name: str) -> bool:
        if (
            (self.state_name is None or self.state.cancelable)
            and (new_state_name in self.animations or new_state_name is None)
            and new_state_name != self.state_name
        ):
            self.state_name = new_state_name
            self.start_time = pygame.time.get_ticks()
            return True
        return False
