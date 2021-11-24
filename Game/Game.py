import pygame
from Application import Application
from Game.Objects.Berry import Berry
from Game.Camera import Camera
from Game.Components.Collider import Collider
from Game.Physics import Physics
from Game.Player import Player
from Util.Vec2 import Vec2
from Game.Map import Map


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

        if move.r > 1:
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

        if dir.r > 1:
            dir.r = 1

        scroll = int(input["q"]) - int(input["e"])

        secondary = input["f"]
        primary = input["space"]
        boost = input["lshift"]

        self.player.move(move, dir, scroll, primary, secondary, boost)

    def update(self, timestep: float):
        self.camera.pos = self.player.pos.copy()

        for object in self.objects:
            object.update(timestep)

        self.fps = 1 / timestep

    def render(self, window: pygame.Surface):
        sprites = []

        self.map.render(sprites)

        for object in self.objects:
            object.render(sprites)

        self.camera.draw(window, sprites)

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
