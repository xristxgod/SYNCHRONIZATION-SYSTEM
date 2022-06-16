import asyncio

from art import tprint

from app.binance.scraper import scrape
from src.models import AccountModel
from config import logger


async def run():
    tprint("START BINANCE-BOT-PARSER")
    while True:
        accounts = await AccountModel.all()
        await asyncio.gather(*[
            scrape(api_name=account.api_name, user_id=account.user_id)
            for account in accounts
        ])
        logger.error("SLEEP: 1500 SEC")
        await asyncio.sleep(1500)
