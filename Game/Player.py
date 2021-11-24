import math
import pygame
from Game.Components.Animation import Animation
from Game.Components.Animator import Animator
from Game.Components.ButtonHandler import ButtonHandler
from Game.Components.Collider import Collider
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

        self.boost_animator = Animator(
            "rest",
            [
                Animation(
                    "rest", [Animation.images_from_spritesheet(pygame.image.load(os.path.join("Assets", "boost.png")), 12)[11]], [10], "rest", True
                ),
                Animation(
                    "cooldown",
                    Animation.images_from_spritesheet(pygame.image.load(os.path.join("Assets", "boost.png")), 12),
                    [2 * (1000 / 12)] * 12,
                    "rest",
                    False,
                ),
            ],
        )

        self.scroll_handler = ButtonHandler(150)
        self.primary_handler = ButtonHandler(100)
        self.secondary_handler = ButtonHandler(100)
        self.boost_handler = ButtonHandler(2000)

        self.item_image = pygame.image.load(os.path.join("Assets", "item_slot.png"))
        self.active_item_image = pygame.image.load(os.path.join("Assets", "active_item_slot.png"))

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
    def crystal(self):
        return self.items[0]

    @crystal.setter
    def crystal(self, value):
        self.items[0] = value

    @property
    def crystal_pos(self):
        return self.pos + self.dir * 0.475

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
        self.scroll_handler.update(bool(scroll))
        self.primary_handler.update(primary)
        self.secondary_handler.update(secondary)
        self.boost_handler.update(boost)

        # Crystal Invoking
        if not self.crystal is None:
            self.crystal.invoke(self.item_index == 0 and primary, self, self.crystal_pos, self.dir.copy())

        # Primary (non-crystal)
        if self.primary_handler.value:
            if self.item_index == 0:
                pass
            if self.item_index == 3:  # satchel pickup
                if self.satchel.can_add_item():
                    item = self.try_pickup_item()
                    if not item is None:
                        self.satchel.add_item(item)
            else:
                if self.cur_item is None:
                    self.cur_item = self.try_pickup_item()

        # Secondary
        if self.secondary_handler.value:

            # TODO: make crafting require you to hold [F] and if you just press F you drop crystal??
            # Crafting
            if self.item_index == 0:
                cols = self.game.physics.find_cols(Collider("rect", self.pos + self.dir * 0.5, Vec2(0.6, 0.6), 4), [4])
                new_crystal = self.crystal.try_craft([c.parent for c in cols])
                if not new_crystal is None:
                    for c in cols:
                        self.game.remove_object(c.parent)
                    self.crystal = new_crystal(Vec2(0, 0), self.game)
            # Drop item from satchel
            elif self.item_index == 3:
                if self.cur_item.can_remove_item():
                    item = self.cur_item.remove_item()
                    item.pos.set(self.pos + self.dir * 0.5)
                    self.game.add_object(item)
            # Drop item from hand
            elif not self.cur_item is None:
                self.cur_item.pos.set(self.pos + self.dir * 0.5)
                self.game.add_object(self.cur_item)
                self.cur_item = None

        # Inventory Scrolling
        if self.scroll_handler.value:
            self.item_index = (self.item_index + scroll + len(self.items)) % len(self.items)

        # Boost
        if self.boost_handler.value or self.boost_handler.cooldown_duration < 50:
            self.boost_animator.try_change_state("cooldown")
            self.acc = self.input_vel.normalized() * 100 if self.input_vel.r > 0 else self.dir.normalized() * 70

        # Movement
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

        dist = self.game.physics.move(self.collider, (self.vel + self.input_vel) * timestep, [1])
        if dist == 0:
            self.vel = Vec2(0, 0)

        # TODO: make this a acceleration thing and do physics right
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
            self.satchel.hand_render(*positions[2], sprites)
            positions.pop(2)

        if self.item_index == 0:  # special case for wand + crystal render
            if not self.crystal is None:
                self.crystal.hand_render(self.crystal_pos, self.dir.t, sprites)
        else:  # otherwise front render
            if not self.cur_item is None:
                self.cur_item.hand_render(self.front_pos, self.dir.t, sprites)

        for item in items:  # remaining non-current, non-satchel items
            if not item is None:
                item.hand_render(*positions[0], sprites)
                positions.pop(0)

        if self.game.debug > 2:
            sprites.append(self.collider.sprite)

    def hud_render(self, window: pygame.Surface):
        width, height = window.get_size()
        length = width / 13
        positions = [
            Vec2(width - length * 0.75, height - length * 0.75),
            Vec2(width - length * 2, height - length * 0.75),
            Vec2(width - length * 3, height - length * 0.75),
            Vec2(width - length * 4.25, height - length * 0.75),
        ]
        item_slot_image = pygame.transform.scale(self.item_image, (length, length))
        active_item_slot_image = pygame.transform.scale(self.active_item_image, (length, length))

        for i in range(len(positions)):
            frame = active_item_slot_image if i == self.item_index else item_slot_image
            window.blit(frame, frame.get_rect(center=positions[i].tup))

            if not self.items[i] is None:
                self.items[i].item_render(positions[i], window)

        boost_image = pygame.transform.scale(self.boost_animator.get_image(), (length * 2, length * 2))
        window.blit(boost_image, boost_image.get_rect(center=(length * 0.75, height - length * 1.25)))
