import aiohttp
import asyncio
import json


async def get_day_currency_ondate(date: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.nbrb.by/api/exrates/rates?ondate={date}&periodicity=0') as resp:
            curr = await resp.json()
            return curr


if __name__ == '__main__':
    cur = asyncio.run(get_day_currency_ondate('2022-01-08'))
    pprint(cur)
