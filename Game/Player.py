import math
import pygame
from Game.Components.Collider import Collider
from Game.Components.Cooldown import Cooldown
from Game.Objects.Satchel import Satchel
from Game.Physics import Physics
from Util.Vec2 import Vec2
from Game.Components.Sprite import Sprite
from Game.Objects.FireCrystal import FireCrystal
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

        self.items = [FireCrystal(Vec2(0, 0), self.game), None, None, Satchel(self.game)]
        self.item_index = 0

        self.boost_cooldown = Cooldown(3)
        self.scroll_cooldown = Cooldown(0.2)
        self.primary_cooldown = Cooldown(0.2)
        self.secondary_cooldown = Cooldown(0.2)

        self.item_image = pygame.image.load(os.path.join("Assets", "item_slot.png"))
        self.active_item_image = pygame.image.load(os.path.join("Assets", "active_item_slot.png"))
        self.wand_image = pygame.image.load(os.path.join("Assets", "wand.png"))

    # region getters

    @property
    def cur_item(self):
        return self.items[self.item_index]

    @cur_item.setter
    def cur_item(self, item):
        self.items[self.item_index] = item

    @property
    def satchel(self) -> Satchel:
        return self.items[3]

    @property
    def cur_crystal(self):
        return self.items[0]

    @property
    def wand_pos(self):
        return self.pos + self.dir * 0.4 + self.dir.right() * 0.3

    @property
    def crystal_pos(self):
        return self.pos + self.dir * 0.6 + self.dir.right() * 0.1

    @property
    def shoot_pos(self):
        return self.pos + self.dir * 0.6

    @property
    def front_pos(self):
        return self.pos + self.dir * 0.45

    @property
    def right_hip_pos_1(self):
        return self.pos + self.dir * 0.15 + self.dir.right() * 0.3

    @property
    def right_hip_pos_2(self):
        return self.pos - self.dir * 0.15 + self.dir.right() * 0.3

    @property
    def left_hip_pos(self):
        return self.pos + self.dir.left() * 0.3

    # endregion

    def try_pickup_item(self):
        cols = self.game.physics.find_cols(Collider("rect", self.pos + self.dir * 0.5, Vec2(0.6, 0.6), 4), [4])
        if len(cols) > 0:
            self.game.remove_object(cols[0].parent)
            return cols[0].parent
        return None

    def move(self, move: Vec2, dir: Vec2, scroll: int, primary: bool, secondary: bool, boost: bool):
        if primary and self.primary_cooldown.ready():
            if self.item_index == 0:
                if not self.cur_crystal is None:
                    self.cur_crystal.invoke(self, self.shoot_pos, self.dir)
            elif self.item_index == 3:  # satchel pickup
                if self.satchel.can_add_item():
                    item = self.try_pickup_item()
                    if not item is None:
                        self.satchel.add_item(item)
            else:
                if self.cur_item is None:
                    self.primary_down = True
                    self.cur_item = self.try_pickup_item()

        if secondary and self.secondary_cooldown.ready():
            if self.item_index == 0:
                pass
            elif self.item_index == 3:
                if self.cur_item.can_remove_item():
                    item = self.cur_item.remove_item()
                    item.pos.set(self.pos + self.dir * 0.5)
                    self.game.add_object(item)
            else:
                if self.cur_item is None:
                    pass
                else:
                    self.cur_item.pos.set(self.pos + self.dir * 0.5)
                    self.game.add_object(self.cur_item)
                    self.cur_item = None

        if scroll and self.scroll_cooldown.ready():
            self.item_index = (self.item_index + scroll + 4) % 4

        if boost and (self.boost_cooldown.ready() or self.boost_cooldown.within(0.075)):
            self.acc = self.input_vel.normalized() * 100 if self.input_vel.r > 0 else self.dir.normalized() * 70

        self.input_vel = move * (self.input_vel.r + 0.2)
        if dir.r > 0:
            self.dir = dir
        elif self.input_vel.r > 0:  # TODO: should this be removed??
            self.dir = self.input_vel.normalized()

    def update(self, timestep: float):
        # cap move velocity
        if self.input_vel.r > 2:
            self.input_vel.r = 2

        self.vel += self.acc * timestep
        self.acc = 0

        self.game.physics.move(self.collider, (self.vel + self.input_vel) * timestep, [1])

        self.vel -= self.vel * 0.1

        self.sprite.angle = self.dir.t

    def render(self, sprites: list[Sprite]):
        sprites.append(self.sprite)

        items = self.items.copy()
        items.pop(self.item_index)

        # cur_time = float(pygame.time.get_ticks()) / 1000
        # positions = [cur_time, cur_time + 2 * math.pi / 3, cur_time + 4 * math.pi / 3]
        # positions = [(self.pos + Vec2(0.5, 0).rotate(t), t) for t in positions]
        positions = [
            (self.right_hip_pos_1, self.dir.right().t),
            (self.right_hip_pos_2, self.dir.right().t),
            (self.left_hip_pos, self.dir.left().t),
        ]

        if self.item_index != 3:  # prioritize satchel on left hip
            items.pop(2)
            self.satchel.item_render(*positions[2], sprites)
            positions.pop(2)

        if self.item_index == 0:  # special case for wand + crystal render
            sprites.append(Sprite(self.wand_image, self.wand_pos, self.dir.right().t + math.pi / 6, Vec2(0.5, 0.5), 2))
            if not self.cur_crystal is None:
                self.cur_crystal.item_render(self.crystal_pos, self.dir.t, sprites)
        else:  # otherwise front render
            if not self.cur_item is None:
                self.cur_item.item_render(self.front_pos, self.dir.t, sprites)

        for item in items:  # remaining non-current, non-satchel items
            if not item is None:
                item.item_render(*positions[0], sprites)
                positions.pop(0)
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
