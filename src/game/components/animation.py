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
