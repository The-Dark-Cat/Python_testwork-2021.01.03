from bot import types, bot, logging


commands = [
    types.BotCommand(command="/start", description="Run this bot"),
    types.BotCommand(command="/list", description="Return values list"),
    types.BotCommand(command="/exchange",
                     description='/exchange <count> USD to <currency>, convert to the second currency'),
    types.BotCommand(command="/history",
                     description='/history USD/<currency> for <count> days, \n'
                     'return an image graph chart which shows the exchange rate graph of the selected currency'),
]
empty = []


async def set_commands():
    await bot.set_my_commands(empty)
    await bot.set_my_commands(commands)
    logging.info('Commands set complete')
