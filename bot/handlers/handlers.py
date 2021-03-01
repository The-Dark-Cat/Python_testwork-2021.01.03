from bot import dp, types, bot
from aiogram.dispatcher import FSMContext

import time
import os

from bot import exchangeratesapi
from ..DB import Connection, init_db

init_db()


@dp.message_handler(commands='start')
async def start(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Hi, I\'m a bot.'
                                        'I can tell you the current exchange rate, calculate how much foreign '
                                        'currency you can buy with your money, and even show a graph of the value '
                                        'of any currency. To see a list of commands just type "/"')


@dp.message_handler(commands='list')
async def list_cmd(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    connection = Connection()
    if time.time() - user_data.get('last_request', 0.0) < 600:
        lst = await exchangeratesapi.get_values_fjson(connection.get_all())
    else:
        try:
            json, lst = await exchangeratesapi.list_()
        except KeyError:
            await msg.answer('Sorry. We do not have data for this range')
            return
        connection.write(json)
        await state.update_data(last_request=time.time())
    await bot.send_message(msg.chat.id, 'Values rate:\n' + '\n'.join(lst))


@dp.message_handler(commands='exchange')
async def exchange(msg: types.Message, state: FSMContext):
    re = await exchangeratesapi.re_exchange(msg.text)
    if not re:
        await msg.answer('You may have missed something. Correctly it will be like this:\n'
                         '/exchange <count> USD to <currency>\n'
                         'This command convert to the second currency')
        return
    user_data = await state.get_data()
    count, currency = re
    connection = Connection()
    if time.time() - user_data.get('last_request', 0.0) < 600:
        course = connection.get(currency)[0]
    else:
        json = await exchangeratesapi.request('https://api.exchangeratesapi.io/latest?base=USD')
        try:
            json = await exchangeratesapi.clrjson(json)
        except KeyError:
            await msg.answer('Sorry. We do not have data for this range')
            return
        course = json[currency]
        connection.write(json)
        await state.update_data(last_request=time.time())
    await msg.answer(f'''{currency}: {round(float(count) * course, 2)}''')


@dp.message_handler(commands='history')
async def history(msg: types.Message):
    re = await exchangeratesapi.re_history(msg.text)
    if not re:
        await msg.answer('You may have missed something. Correctly it will be like this:\n'
                         '/history USD/<currency> for <count> days\n'
                         'This command return an image graph chart which shows '
                         'the exchange rate graph of the selected currency')
        return
    count, currency = re
    try:
        path = await exchangeratesapi.get_timedelta(count, currency)
    except KeyError:
        await msg.answer('Sorry. We do not have data for this range')
        return
    await bot.send_photo(msg.chat.id, photo=open(path, 'rb'))
    os.remove(path)


@dp.message_handler(content_types='text')
async def hello(msg: types.Message):
    if 'hello' in msg.text.lower():
        await bot.send_message(msg.chat.id, 'Hello!!!')
    elif '/' in msg.text:
        await bot.send_message(msg.chat.id, 'I\'m not sure I understand this command. '
                                            'Maybe you should try again or see the list of supported commands, '
                                            'just type "/"')
    else:
        await bot.send_message(msg.chat.id, 'Hi...Sorry, '
                                            'I don\'t quite understand you, you\'d better use the commands, '
                                            'they start with a "/"')
