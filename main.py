import asyncio 
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import dotenv_values
import logging

config = dotenv_values('.env')

token = '8002413360:AAHYytB_C4_hJUckZz82T9dgifOg3kLHTZQ'
bot = Bot(token=token)
dp = Dispatcher()

unique_users = set()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    unique_users.add(user_id)
    user_count = len(unique_users)
    name = message.from_user.first_name
    await message.answer(f'Привет, {name}! Наш бот уже обслуживает {user_count} пользователей')

@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "неизвестный"
    await message.answer(f"Ваш id: {user_id}\nВаше имя: {first_name}\nВаш ник: @{username}")

@dp.message(Command("random"))
async def random_handler(message: types.Message):
    names = ['Карина', 'Диана', 'Алина', 'Бека', 'Рената']
    random_name = random.choice(names)
    await message.answer(f'Случайное имя: {random_name}')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
