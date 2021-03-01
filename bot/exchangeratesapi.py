import asyncio
import aiohttp
import datetime
import re

from bot import logging
from .plotter import plot

dateformat = '%Y-%m-%d'


async def request(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            logging.info('request return' + (await resp.text())[:45] + '...')
            return await resp.json()


async def get_values_fjson(json):
    """get values from json"""
    return [f'{i}: {round(json[i], 2)}' for i in json if i not in ['base', 'USD']]


async def list_():
    json = await request('https://api.exchangeratesapi.io/latest?base=USD')
    json = await clrjson(json)
    return json, await get_values_fjson(json)


async def clrjson(json):
    '''return clear json'''
    return json['rates']


async def re_exchange(string):
    if re.match(r'/exchange\s*\$\s*\d+\s*to\s*\w{2,3}', string):
        count, val = re.findall(r'/exchange\s*\$\s*(\d+)\s*to\s*(\w+)', string)[0]
        return count, val
    elif re.match(r'/exchange\s*\d+\s*\w{2,3}\s*to\s*\w+', string):
        count, val = re.findall(r'/exchange\s*(\d+)\s*\w{2,3}\s*to\s*(\w+)', string)[0]
        return count, val
    else:
        return False


async def re_history(string):
    if re.match(r'/history\s*\w{2,3}/\w{2,3}\s*for\s*\d+\s*days', string):
        curr, count = re.findall(r'/history\s*\w{2,3}/(\w{2,3})\s*for\s*(\d+)\s*days', string)[0]
        return int(count), curr
    else:
        return False


async def get_timedelta(days, currency):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)

    res = await request('https://api.exchangeratesapi.io/history?'
                        f'start_at={start_date.strftime(dateformat)}&'
                        f'end_at={today.strftime(dateformat)}&base=USD&symbols={currency}')
    rates = await rate_sort(res, currency)
    return await plot([rate[0] for rate in rates], [rate[1] for rate in rates], currency)


async def rate_sort(json, currency):
    json = json['rates']
    rates = [(datetime.datetime.strptime(rate[0], dateformat), rate[1][currency]) for rate in json.items()]
    sorted_rates = await quick_sort(rates)
    rates = [(rate[0].strftime(dateformat)[5:], rate[1]) for rate in sorted_rates]
    return rates


async def quick_sort(rates):
    if len(rates) <= 1:
        return rates
    base = rates[0][0]
    left = [i for i in rates if i[0] < base]
    center = [i for i in rates if i[0] == base]
    right = [i for i in rates if i[0] > base]

    return await quick_sort(left) + center + await quick_sort(right)


if __name__ == '__main__':
    aioloop = asyncio.get_event_loop()
    aioloop.run_until_complete(get_timedelta('RUB', 30))
