import math
import pygame
from Game.Components.Collider import Collider
from Game.Objects.Satchel import Satchel
from Game.Physics import Physics
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite
import os


class Player:
    def __init__(self, pos: Vec2, game):
        self.pos = pos
        self.vel = Vec2(0, 0)
        self.acc = Vec2(0, 0)
        self.input_vel = Vec2(0, 0)
        self.dir = Vec2(1, 0)

        self.collider = Collider("circle", self.pos, 0.4, 2, self)
        self.game = game

        self.sprite = Sprite(pygame.image.load(os.path.join("Assets", "player.png")), self.pos, 0, Vec2.one(), 2)

        self.items = [None, None, None, Satchel(self.game)]

        self.boost_cooldown = 0
        self.boost_frames = 3

        self.item_index = 0
        self.item_switch_cooldown = 0

        self.item_image = pygame.image.load(os.path.join("Assets", "item_slot.png"))
        self.active_item_image = pygame.image.load(os.path.join("Assets", "active_item_slot.png"))

        self.primary_down = False

    def try_pickup_item(self):
        cols = self.game.physics.find_cols(Collider("rect", self.pos + self.dir * 0.5, Vec2(0.6, 0.6), 4), [4])
        if len(cols) > 0:
            self.game.remove_object(cols[0].parent)
            return cols[0].parent
        return None

    def move(self, move: Vec2, dir: Vec2, scroll: int, primary: bool, secondary: bool, boost: bool):
        self.primary_down = False
        if primary:
            if self.item_index == 0:
                pass  # shoot
            elif self.item_index == 3:  # satchel pickup
                if self.items[self.item_index].can_add_item():
                    item = self.try_pickup_item()
                    if not item is None:
                        self.items[self.item_index].add_item(item)
            else:
                if self.items[self.item_index] is None:
                    self.primary_down = True
                    self.items[self.item_index] = self.try_pickup_item()

        if secondary:
            if self.item_index == 0:
                pass
            elif self.item_index == 3:
                if self.items[self.item_index].can_remove_item():
                    item = self.items[self.item_index].remove_item()
                    item.pos.set(self.pos + self.dir * 0.5)
                    self.game.add_object(item)
            else:
                if self.items[self.item_index] is None:
                    pass
                else:
                    self.items[self.item_index].pos.set(self.pos + self.dir * 0.5)
                    self.game.add_object(self.items[self.item_index])
                    self.items[self.item_index] = None

        if scroll and self.item_switch_cooldown == 0:
            self.item_index = (self.item_index + scroll + 4) % 4
            self.item_switch_cooldown = 10
        else:
            self.item_switch_cooldown = max(self.item_switch_cooldown - 1, 0)

        if boost:
            if self.boost_cooldown <= 0:
                self.boost_cooldown = 5
                self.boost_frames = 4
            if self.boost_frames > 0:
                self.acc = self.input_vel.normalized() * 100 if self.input_vel.r > 0 else self.dir.normalized() * 70
                self.boost_frames -= 1

        self.input_vel = move * (self.input_vel.r + 0.2)
        if dir.r > 0:
            self.dir = dir
        elif self.input_vel.r > 0:
            self.dir = self.input_vel.normalized()

    def update(self, timestep: float):
        # cap move velocity
        if self.input_vel.r > 2:
            self.input_vel.r = 2

        self.vel += self.acc * timestep
        self.acc = 0

        if self.boost_cooldown > 0:
            self.boost_cooldown -= timestep

        self.game.physics.move(self.collider, (self.vel + self.input_vel) * timestep, [1])

        self.vel -= self.vel * 0.1

        self.sprite.angle = self.dir.t

    def render(self, sprites: list[Sprite]):
        sprites.append(self.sprite)
        if self.primary_down:
            sprites.append(Collider("rect", self.pos + self.dir * 0.5, Vec2(0.6, 0.6), 4).sprite)

        if self.item_index != 0 and not self.items[self.item_index] is None:
            sprites.append(Sprite(self.items[self.item_index].image, self.pos + self.dir * 0.5, self.dir.t + 3 * math.pi / 2, Vec2(0.4, 0.4), 2))
        # sprites.append(self.collider.sprite)

    def hud_render(self, window: pygame.Surface):
        width, height = window.get_size()
        length = width / 13
        positions = [
            (width - length * 0.75, height - length * 0.75),
            (width - length * 2, height - length * 0.75),
            (width - length * 3, height - length * 0.75),
            (width - length * 4.25, height - length * 0.75),
        ]
        item_slot_image = pygame.transform.scale(self.item_image, (length, length))
        active_item_slot_image = pygame.transform.scale(self.active_item_image, (length, length))

        for i in range(len(positions)):
            frame = active_item_slot_image if i == self.item_index else item_slot_image
            window.blit(frame, frame.get_rect(center=positions[i]))

            if not self.items[i] is None:
                item = pygame.transform.scale(self.items[i].image, (length * 0.75, length * 0.75))
                window.blit(item, item.get_rect(center=positions[i]))
