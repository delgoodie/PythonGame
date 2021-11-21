import pygame


class Input:
    # TODO: Write docs for Input class
    """
    Doc for Input
    """

    def __init__(self):
        self._pressed = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "shift": False,
            "space": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "e": False,
        }
        self.up = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
        }
        self.down = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
        }

    def __getitem__(self, key: str):
        return self._pressed[key]

    def __setitem__(self, key: str, value: bool):
        self._pressed[key] = value

    def __delitem__(self, key: str):
        del self._pressed[key]

    def read(self, events):
        self.clear()

        # ON KEYUP & ON KEYDOWN events
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.down[e.unicode] = True
            elif e.type == pygame.KEYUP:
                self.up[e.unicode] = True

        # KEY CURRENTLY PRESSED
        keys_pressed = pygame.key.get_pressed()

        # TODO: Add support for more keys pressed
        if keys_pressed[pygame.K_w]:
            self["w"] = True
        if keys_pressed[pygame.K_a]:
            self["a"] = True
        if keys_pressed[pygame.K_s]:
            self["s"] = True
        if keys_pressed[pygame.K_d]:
            self["d"] = True
        if keys_pressed[pygame.K_LSHIFT]:
            self["shift"] = True
        if keys_pressed[pygame.K_SPACE]:
            self["space"] = True
        if keys_pressed[pygame.K_LEFT]:
            self["left"] = True
        if keys_pressed[pygame.K_RIGHT]:
            self["right"] = True
        if keys_pressed[pygame.K_UP]:
            self["up"] = True
        if keys_pressed[pygame.K_DOWN]:
            self["down"] = True
        if keys_pressed[pygame.K_e]:
            self["e"] = True

    def clear(self):
        for key in self._pressed:
            self._pressed[key] = False

        for key in self.up:
            self.up[key] = False

        for key in self.down:
            self.down[key] = False
