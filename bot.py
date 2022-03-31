import json
import os

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TGTOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Избранные', 'Основные', 'Остальные']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Курсы валют НБ РБ на сегодня', reply_markup=keyboard)


@dp.message_handler(Text(equals='Избранные'))
async def all_currency(message: types.Message):
    with open('./data/favorite_currencies.json') as file:
        data = json.load(file)
        s = f""
        for i in data:
            for k, v in i.items():
                s += f"{v['Cur_Name']}: {v['Cur_OfficialRate']} BYN / {v['Cur_Scale']} {k}\n"
        await message.reply(s)


@dp.message_handler(Text(equals='Основные'))
async def all_currency(message: types.Message):
    with open('./data/day_all_currencies.json') as file:
        data = json.load(file)
        s = f""
        for v in data:
            s += f"{v['Cur_Name']}: {v['Cur_OfficialRate']} BYN / {v['Cur_Scale']} {v['Cur_Abbreviation']}\n"
        await message.reply(s)


@dp.message_handler(Text(equals='Остальные'))
async def all_currency(message: types.Message):
    with open('./data/month_all_currencies.json') as file:
        data = json.load(file)
        s = f"*** На дату {data[0]['Date'][:10]} ***\n"
        for v in data:
            s += f"{v['Cur_Name']}: {v['Cur_OfficialRate']} BYN / {v['Cur_Scale']} {v['Cur_Abbreviation']}\n"
        await message.reply(s)


if __name__ == '__main__':
    executor.start_polling(dp)
