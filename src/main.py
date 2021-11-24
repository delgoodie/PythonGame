from application import Application
from game.game import Game


def main():
    app = Application("settings.csv")
    game = Game()

    app.run(game.loop)


if __name__ == "__main__":
    main()
