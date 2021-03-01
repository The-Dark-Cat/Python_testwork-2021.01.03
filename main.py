from bot import dp, executor
import asyncio

from bot import handlers, commands


aioloop = asyncio.get_event_loop()
aioloop.create_task(commands.set_commands())

if __name__ == '__main__':
    executor.start_polling(dp)
