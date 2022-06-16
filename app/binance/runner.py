import time
import asyncio
from datetime import datetime, timedelta
from typing import List, Tuple

from art import tprint

from app.db import init
from app.binance.scraper import scrape
from src.models import AccountModel
from src.types import API_NAME
from config import Config, logger


async def run():
    """Works endlessly"""
    await init()
    tprint("BINANCE-BOT-PARSER", font="bulbhead")
    while True:
        start_iteration_time = time.time()
        logger.error(f"{datetime.now()} | START ITERATION")
        accounts = await AccountModel.all()
        await asyncio.gather(*[
            scrape(api_name=account.api_name, user_id=account.user_id)
            for account in accounts
        ])
        logger.error((
            f"{datetime.now()} | END ITERATION | "
            f"TIME ELAPSED: {timedelta(seconds=time.time() - start_iteration_time)} | SLEEP: {Config.SLEEP_TIME}"
        ))
        await asyncio.sleep(1500)


async def run_by_accounts(accounts: List[Tuple[API_NAME, int]]):
    """Works for a list of accounts!"""
    await init()
    start = time.time()
    tprint("BINANCE-PARSER", font="bulbhead")
    logger.error(f"{datetime.now()} | START PARSER")
    await asyncio.gather(*[
            scrape(api_name=account[0], user_id=account[1])
            for account in accounts
        ])
    logger.error(f"{datetime.now()} | END PARSER | TIME ELAPSED: {timedelta(seconds=time.time() - start)}")
