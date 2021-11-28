import pygame
from application import Application
from game.components.shapes import Rects, Sprite
from game.objects.ingredients.berry import Berry
from game.camera import Camera
from game.physics import Physics
from game.objects.player import Player
from util.vec2 import Vec2
from game.map import Map


class Game:
    def __init__(self):
        self.objects = []
        self.physics = Physics([])
        self.debug = 0

        self.player = Player(Vec2(1, 1), self)
        self.add_object(self.player)

        self.add_object(Berry(Vec2(3, 1), self))
        self.add_object(Berry(Vec2(4, 1), self))

        self.camera = Camera(Vec2(2, 0), 10)
        self.map = Map("path", self)

        self.fps = 0

    def add_object(self, obj):
        self.objects.append(obj)
        if hasattr(obj, "collider"):
            self.physics.colliders.append(obj.collider)

    def remove_object(self, obj):
        if hasattr(obj, "collider"):
            self.physics.colliders.remove(obj.collider)
        self.objects.remove(obj)

    def handle_input(self, input):
        move = Vec2(0, 0)
        if input["a"]:
            move.x -= 1
        if input["d"]:
            move.x += 1
        if input["w"]:
            move.y += 1
        if input["s"]:
            move.y -= 1

        if move.sqrMag > 1:
            move.r = 1

        dir = Vec2(0, 0)
        if input["j"]:
            dir.x -= 1
        if input["l"]:
            dir.x += 1
        if input["i"]:
            dir.y += 1
        if input["k"]:
            dir.y -= 1

        if dir.sqrMag > 1:
            dir.r = 1

        scroll = int(input["q"]) - int(input["e"])

        secondary = input["f"]
        primary = input["space"]
        boost = input["lshift"]

        self.player.move(move, dir, scroll, primary, secondary, boost)

    def update(self, timestep: int):
        self.camera.pos = self.player.pos.copy()

        for object in self.objects:
            object.update(timestep)

        self.fps = 1 / (timestep / 1000)

    def render(self, window: pygame.Surface):
        shapes: list[Sprite | Rects] = []

        self.map.render(shapes)

        for object in self.objects:
            object.render(shapes)

        self.camera.draw(window, shapes)
        self.camera.draw_shadows(window, self.physics.colliders)

    def hud_render(self, window):
        self.player.hud_render(window)
        fps_font = pygame.font.SysFont("Comic Sans MS", 30)
        textsurface = fps_font.render(str(round(self.fps)), True, (0, 0, 0))
        window.blit(textsurface, (20, 20))

    def loop(self, app: Application):
        self.handle_input(app.input)

        self.update(app.timestep)

        self.render(app.window)

        self.hud_render(app.window)
