from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import configfile
import logging


bot = Bot(token=configfile.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO, format='[%(levelname)s][%(asctime)s]: %(message)s')
