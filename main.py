import sys
import argparse

from art import tprint

from app.db import init


class Parser:
    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--interface", default=None)
        parser.add_argument("-a", "--account", default=None)
        return parser

    @staticmethod
    async def run_sys(data):
        pass

    @staticmethod
    async def run_input():
        pass


if __name__ == '__main__':
    """PARSER BOT BINANCE/BYBIT"""
    namespace = Parser.create_parser().parse_args(sys.argv[1:])
    tprint("PARSER BOT BINANCE/BYBIT", font="bulbhead")
    if namespace.interface:
        pass
    elif namespace.account:
        pass
    else:
        pass

