# -*- coding: utf-8 -*-

# import built-in modules
import argparse
import logging
import sys

# import third-party modules

# import your own module
from trackswitchinggame.game import Game

VERSION = "0.1"
APP_NAME = "Track Switching Game"
APP_DESCRIPTION = "Prototype of a track switching game."


def parse_argv() -> dict:
    """
    Parse command-line arguments into a dict.
    """
    arg_parser = argparse.ArgumentParser(prog=APP_NAME, description=APP_DESCRIPTION)
    arg_parser.add_argument("-d", "--debug", action="store_true", required=False, default=False,
                            help="display debug logging lines")
    args = arg_parser.parse_args()
    args_dict = vars(args)
    return args_dict


# Script starts here
if __name__ == '__main__':
    # Parse command line arguments
    args = parse_argv()

    # Set-up logging
    if args["debug"]:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(level=logging_level)

    print(f"{APP_NAME} v{VERSION}")

    # Set-up and run game
    game = Game()
    game.run()

    sys.exit()
