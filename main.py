import pygame
import os
from Application import Application
from Game.Player import Player
from Util.Vec2 import Vec2
from Game.Game import Game


def main():
    app = Application("settings.csv")
    game = Game()

    app.run(game.loop)


if __name__ == "__main__":
    main()


# pygame.draw.polygon(surface, color, pointlist, width)
# pygame.draw.line(surface, color, start_point, end_point, width)
# pygame.draw.lines(surface, color, closed, pointlist, width)
# pygame.draw.circle(surface, color, center_point, radius, width)
# pygame.draw.ellipse(surface, color, bounding_rectangle, width)
# pygame.draw.rect(surface, color, rectangle_tuple, width)


# pygame.mouse.set_visible(False)


# pause_font = pygame.font.Font(s.FONTS["retro_computer"], 64)
# pause_text = pause_font.render("Paused", 1, s.COLOURS["text"])
# x          = (s.DIMENSIONS[0] - pause_text.get_width()) / 2
# y          = (s.DIMENSIONS[1] - pause_text.get_height()) / 2

# self.window.fill(s.COLOURS["black"])
# self.window.blit(pause_text, (x, y))


# pygame.mixer.music.unpause()


# def render_text(text, window, font, color, position):
#     """Renders a font and blits it to the given window"""
#     text = font.render(text, 1, color)

#     window.blit(text, position)

#     return text


# if os.path.isfile("swervin_mervin/settings_local.py"):
#     execfile("swervin_mervin/settings_local.py")
