import pygame
import os

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

FPS = 60

GUY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "guy.png")), (440 / 4, 360 / 4))

program_active = True

guy_rect = pygame.Rect(100, 100, 440 / 4, 360 / 4)

pygame.display.set_caption("GAME")

Input = {
    "w": False,
    "a": False,
    "s": False,
    "d": False,
    "down": {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
    },
    "up": {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
    },
}


def event_handler():
    global program_active

    for key in Input:
        if not key in ["down", "up"]:
            Input[key] = False
    for key in Input["down"]:
        Input["down"][key] = False
    for key in Input["up"]:
        Input["up"][key] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_active = False
        if event.type == pygame.KEYDOWN:
            Input["down"][event.unicode] = True

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_w]:
        Input["w"] = True
    if keys_pressed[pygame.K_a]:
        Input["a"] = True
    if keys_pressed[pygame.K_s]:
        Input["s"] = True
    if keys_pressed[pygame.K_d]:
        Input["d"] = True


def main():
    global x
    global y
    clock = pygame.time.Clock()
    while program_active:
        clock.tick(FPS)

        event_handler()

        if Input["a"]:
            guy_rect.x -= 3
        if Input["d"]:
            guy_rect.x += 3
        if Input["w"]:
            guy_rect.y -= 3
        if Input["s"]:
            guy_rect.y += 3

        WIN.fill((255, 255, 0))
        WIN.blit(GUY, guy_rect)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
