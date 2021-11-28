import math
import pygame
from game.components.animation import Animation, Animator
from game.components.button_handler import ButtonHandler
from game.components.collider import Collider
from game.objects.particle import Particle
from game.objects.satchel import Satchel
from game.physics import Physics
from util.vec2 import Vec2
from game.components.shapes import Rects, Sprite
from game.objects.crystals.fire_crystal import FireCrystal
import os


class Player:
    def __init__(self, pos: Vec2, game):
        self.pos = pos
        self.vel = Vec2(0, 0)
        self.acc = Vec2(0, 0)
        self.input_vel = Vec2(0, 0)
        self.dir = Vec2(1, 0)
        self.disp = Vec2(0, 0)

        self.collider = Collider("circle", self.pos, 0.4, 2, self)
        self.game = game

        self.sprite = Sprite(pygame.image.load(os.path.join("Assets", "player.png")), self.pos, 0, Vec2.one(), 2)

        self.items = [FireCrystal(Vec2(0, 0), self.game), None, None, Satchel(self.game)]
        self.item_index = 0

        self.boost_bar_animator = Animator(
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

        self.boost_lines_animator = Animator(
            None,
            [
                Animation(
                    "boost",
                    Animation.images_from_spritesheet(pygame.image.load(os.path.join("Assets", "boost_lines.png")), 5),
                    [0.5 * (1000 / 5)] * 5,
                    None,
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

        self.distance = 0

        self.dist_int = 0
        self.right_dust = False

        self.boost_dir = Vec2(0, 0)

        self.health = 11
        self.heart_image = pygame.image.load(os.path.join("Assets", "heart.png"))
        self.half_heart_image = pygame.image.load(os.path.join("Assets", "half_heart.png"))

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
            self.boost_bar_animator.try_change_state("cooldown")
            self.acc = self.input_vel.normalized() * 100 if self.input_vel.sqrMag > 0 else self.dir.normalized() * 70
            self.boost_lines_animator.try_change_state("boost")
            self.boost_dir = self.input_vel.normalized() if self.input_vel.sqrMag > 0 else self.dir.copy()

        # Movement
        self.input_vel = move * (self.input_vel.r + 0.2)

        # Direction
        if self.boost_lines_animator.state is None:
            if dir.sqrMag > 0:
                self.dir = dir
            elif self.input_vel.sqrMag > 0:  # TODO: should this be removed??
                self.dir = self.input_vel.normalized()
        else:
            self.dir = self.boost_dir

    def update(self, timestep: int):
        # cap move velocity
        if self.input_vel.sqrMag > 2 ** 2:
            self.input_vel.r = 2

        self.vel += self.acc * (timestep / 1000)
        self.acc = 0

        dist = self.game.physics.move(self.collider, (self.vel + self.input_vel) * (timestep / 1000), [1])
        if dist == 0:
            self.vel = Vec2(0, 0)

        self.distance += dist

        self.disp = (self.vel + self.input_vel).normalized() * dist

        self.vel -= self.vel * 0.1

        self.sprite.angle = self.dir.t

        if int(self.distance * 1.4) > self.dist_int:
            pos = (
                self.pos
                - self.input_vel.normalized() * 0.3
                + (self.input_vel.right() if self.right_dust else self.input_vel.left()).normalized() * 0.15
            )
            self.game.add_object(
                Particle(
                    pos,
                    self.game,
                    120,
                    -self.input_vel.normalized(),
                    gain=math.pi * 2,
                    lifetime=220,
                    vel=0.03,
                    size=0.1,
                    rate=0.1,
                    disp=0.02,
                    acc=-0.5,
                )
            )
            self.dist_int += 1
            self.right_dust = not self.right_dust

    def render(self, shapes: list[Sprite | Rects]):
        shapes.append(self.sprite)

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
            self.satchel.hand_render(*positions[2], shapes)
            positions.pop(2)

        if self.item_index == 0:  # special case for wand + crystal render
            if not self.crystal is None:
                self.crystal.hand_render(self.crystal_pos, self.dir.t, shapes)
        else:  # otherwise front render
            if not self.cur_item is None:
                self.cur_item.hand_render(self.front_pos, self.dir.t, shapes)

        for item in items:  # remaining non-current, non-satchel items
            if not item is None:
                item.hand_render(*positions[0], shapes)
                positions.pop(0)

        if self.game.debug > 2:
            shapes.append(self.collider.sprite)

        boost_lines_image = self.boost_lines_animator.get_image()
        if boost_lines_image and self.disp.sqrMag > 0:
            shapes.append(Sprite(boost_lines_image, self.pos - self.boost_dir * 0.6, self.boost_dir.t + 3 * math.pi / 2, Vec2(0.5, 0.9), layer=2))
            # shapes.append(Sprite(boost_lines_image, self.pos + self.dir * 0.35, self.dir.t + 3 * math.pi / 2, Vec2(0.6, 0.4), layer=2))

    def hud_render(self, window: pygame.Surface):
        width, height = window.get_size()
        length = width / 13

        # region Inventory
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
        # endregion

        # Boost Bar
        boost_image = pygame.transform.scale(self.boost_bar_animator.get_image(), (length * 2, length * 2))
        window.blit(boost_image, boost_image.get_rect(center=(length * 0.75, height - length * 1.25)))

        # Health
        heart_image = pygame.transform.scale(self.heart_image, (length / 2, length / 2))
        window.blits([(heart_image, (width - length / 2 * (x + 1), length / 4)) for x in range(self.health // 2)])
        if self.health % 2:
            half_heart_image = pygame.transform.scale(self.half_heart_image, (length / 2, length / 2))
            window.blit(half_heart_image, (width - length / 2 * (self.health // 2 + 1), length / 4))
