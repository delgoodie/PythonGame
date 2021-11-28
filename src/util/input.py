import pygame


INIT_KEY_DICT = {
    "w": False,
    "a": False,
    "s": False,
    "d": False,
    "lshift": False,
    "space": False,
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "q": False,
    "e": False,
    "f": False,
    "h": False,
    "j": False,
    "k": False,
    "u": False,
    "i": False,
    "l": False,
}


class Input:
    """
    Doc for Input
    """

    def __init__(self):
        self._pressed = INIT_KEY_DICT.copy()
        self.up = INIT_KEY_DICT.copy()
        self.down = INIT_KEY_DICT.copy()

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
                if e.unicode.isalnum():
                    self.down[e.unicode.lower()] = True
                    self._pressed[e.unicode.lower()] = True
                else:
                    if e.key == pygame.K_SPACE:
                        self.down["space"] = True
                        self._pressed["space"] = True
                    elif e.key == pygame.K_UP:
                        self.down["up"] = True
                        self._pressed["up"] = True
                    elif e.key == pygame.K_DOWN:
                        self.down["down"] = True
                        self._pressed["down"] = True
                    elif e.key == pygame.K_LEFT:
                        self.down["left"] = True
                        self._pressed["left"] = True
                    elif e.key == pygame.K_RIGHT:
                        self.down["right"] = True
                        self._pressed["right"] = True
                    elif e.key == pygame.K_LSHIFT:
                        self.down["lshift"] = True
                        self._pressed["lshift"] = True

            elif e.type == pygame.KEYUP:
                if e.unicode.isalnum():
                    self.down[e.unicode.lower()] = False
                    self._pressed[e.unicode.lower()] = False
                else:
                    if e.key == pygame.K_SPACE:
                        self.down["space"] = False
                        self._pressed["space"] = False
                    elif e.key == pygame.K_UP:
                        self.down["up"] = False
                        self._pressed["up"] = False
                    elif e.key == pygame.K_DOWN:
                        self.down["down"] = False
                        self._pressed["down"] = False
                    elif e.key == pygame.K_LEFT:
                        self.down["left"] = False
                        self._pressed["left"] = False
                    elif e.key == pygame.K_RIGHT:
                        self.down["right"] = False
                        self._pressed["right"] = False
                    elif e.key == pygame.K_LSHIFT:
                        self.down["lshift"] = False
                        self._pressed["lshift"] = False

    def clear(self):
        for key in self.up:
            self.up[key] = False

        for key in self.down:
            self.down[key] = False
