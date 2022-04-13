import json
import os
import re
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

storage = MemoryStorage()

bot = Bot(token=os.getenv('TGTOKEN'))
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp):
    print('Bot started')


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons1 = ['Избранные', 'Основные']
    start_buttons2 = ['Остальные', 'На дату']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons1).add(*start_buttons2)

    await message.answer('Курсы валют НБ РБ', reply_markup=keyboard)


@dp.message_handler(filters.Text(equals='Избранные'))
async def all_currency(message: types.Message):
    with open('./data/favorite_currencies.json') as file:
        data = json.load(file)
        
        s = f"***** На дату {data[0].get('Date')[:10]} *****\n"
        for i in data:
            s += f"{i['Cur_Name']}: {i['Cur_OfficialRate']} BYN / {i['Cur_Scale']} {i['Cur_Abbreviation']}\n"
        await message.reply(s)


@dp.message_handler(filters.Text(equals='Основные'))
async def all_currency(message: types.Message):
    with open('./data/day_all_currencies.json') as file:
        data = json.load(file)
        
        s = f"***** На дату {data[0]['Date'][:10]} *****\n"
        for v in data:
            s += f"{v['Cur_Name']}: {v['Cur_OfficialRate']} BYN / {v['Cur_Scale']} {v['Cur_Abbreviation']}\n"
        await message.reply(s)


@dp.message_handler(filters.Text(equals='Остальные'))
async def all_currency(message: types.Message):
    with open('./data/month_all_currencies.json') as file:
        data = json.load(file)
        
        s = f"***** На дату {data[0]['Date'][:10]} *****\n"
        for v in data:
            s += f"{v['Cur_Name']}: {v['Cur_OfficialRate']} BYN / {v['Cur_Scale']} {v['Cur_Abbreviation']}\n"
        await message.reply(s)


class FSMOnDate(StatesGroup):
    date = State()


@dp.message_handler(Text(equals='На дату'), state=None)
async def get_date(message: types.Message):
    await FSMOnDate.date.set()
    await message.reply('Введите дату в формате ГГГГ-ММ-ДД')
    

@dp.message_handler(commands='отмена', state="*")
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отменено")


@dp.message_handler(state=FSMOnDate.date)
async def get_currency_on_date(date: types.Message, state: FSMContext):
    
    in_date = str(date.text)
    if not re.match(r'\d{4}-\d{2}-\d{2}', in_date):
        await date.reply('Неверный формат даты')
        await state.finish()
        return
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.nbrb.by/api/exrates/rates?ondate={in_date}&periodicity=0') as resp:
                level = await resp.json()
                s = f"***** На дату {level[0]['Date'][:10]} *****\n"
                
                for curr in level:
                    s += f"{curr['Cur_Name']}: {curr['Cur_OfficialRate']} BYN / {curr['Cur_Scale']} {curr['Cur_Abbreviation']}\n"
                await date.reply(s)
                await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
