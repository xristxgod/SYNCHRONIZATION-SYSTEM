import sys
import asyncio
import argparse
from typing import List, Tuple

from art import tprint

from app.binance.runner import run as run_binance, run_by_accounts as run_by_accounts_binance
from src.types import API_NAME
from src.utils.utils import utils
from config import Config, logger


manual = f"""
    ADMIN TOOLS V{Config.VERSION}
    Supported command list
    list                                        get a list of users and their accounts
    list [user]                                 get a list of account of this user
    set_balance [user] [balance]                assign balance to specified user
    delete [user]                               deletes specified user and associated data
    
    parser user [user]                          go through all the accounts of this user
    parser user [user] account [account]        go through these accounts of this user.
    parser users [user,user]                    go through the user data accounts
    parser accounts [account, account]          go through these accounts
                    
    quit, --quit, -q                    exists the program  
    help, --help, -h                    prints this text\n\n       
"""


class Parser:
    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--interface", default=None)
        parser.add_argument("-n", "--network", default="binance")
        parser.add_argument("-a", "--account", default=None)
        return parser

    @staticmethod
    async def run_sys(accounts: List[Tuple[API_NAME, int]], network: str = "binance"):
        if network == "binance":
            await run_by_accounts_binance(accounts=accounts)

    @staticmethod
    def run_input():
        pass


if __name__ == '__main__':
    """PARSER BOT BINANCE/BYBIT"""
    _parser = Parser
    namespace = Parser.create_parser().parse_args(sys.argv[1:])
    tprint("PARSER/BOT | BINANCE/BYBIT", font="bulbhead")
    if namespace.interface:
        _parser.run_input()
    elif namespace.account and namespace.network in ["binance", "bybit"]:
        asyncio.run(_parser.run_sys(
            accounts=utils.correct_parser_data(data=namespace.account, _type=list), network=namespace.network
        ))
    else:
        asyncio.run(run_binance())
    logger.error("GOOD BYE!")
