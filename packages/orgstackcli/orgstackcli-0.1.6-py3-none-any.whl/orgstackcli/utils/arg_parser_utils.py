import argparse

from ..config import settings


def init_arg_parser():
    parser = argparse.ArgumentParser(prog=settings.CLI_PROGRAM_NAME)
    parser.add_argument(
        "command",
        type=str,
        help="Command to run",
        choices=settings.CLI_COMMAND_CHOICES
    )

    return parser
