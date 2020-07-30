"""
Demo 4: Flappy Bird example
---------------------------
@Author: Amardjia Amine
@Date: 10/08/18
@Version: 0.0.2 (beta)

A simple 2D game with laylib and  pygame to show how fast and simple
is to create a multimedia application using the laylib package.
Note that the initialization of pygame and the resources management
are completely transparent and automatic for the developer.

This game must use obsolete laylib version 1.0 (available in the same folder of game)

"""
from laylib import Environment
from engine import FlappyBird


def main():
    # setting up the env
    game = Environment(650, 800, False, 'Flappy Bird Demo')
    game.load_complete(FlappyBird(), 'data', 'resources.bin')
    # play
    game.gInstance.main_loop()
    game.destroy()


if __name__ == '__main__':
    main()


# from laylib.resources import Resources

# def auto_save(enabled=False):
#     res = Resources('data')
#     if enabled:
#         res.save('resources.bin')
