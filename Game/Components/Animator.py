import pygame

from Game.Components.Animation import Animation


class Animator:
    def __init__(self, initial_state_name: str, animations: list[Animation]):
        self.state_name = initial_state_name
        self.start_time = pygame.time.get_ticks()
        self.animations = dict([(anim.name, anim) for anim in animations])

    @property
    def state(self) -> Animation:
        return self.animations[self.state_name]

    def get_image(self):
        while True:
            cur_dur = pygame.time.get_ticks() - self.start_time
            print(self.state_name, cur_dur, self.state.duration)
            if cur_dur < self.state.duration:
                return self.state.get_image(cur_dur)
            else:
                self.start_time += self.state.duration
                self.state_name = self.state.next

    def try_change_state(self, new_state_name: str) -> bool:
        if self.state.cancelable and new_state_name in self.animations:
            if new_state_name != self.state_name:
                self.state_name = new_state_name
                self.start_time = pygame.time.get_ticks()
            return True
        return False
