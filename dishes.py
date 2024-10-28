from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3

from bot_config import database

admin_id = 636715358

class DishForm(StatesGroup):
    name = State()
    price = State()
    category = State()
    confirm = State()

dish_router = Router()

@dish_router.message(Command("add_dish"))
async def start_dish_form(message: types.Message, state: FSMContext):
    if message.from_user.id != admin_id:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    await state.set_state(DishForm.name)
    await message.answer("Задайте название блюда:")

@dish_router.message(DishForm.name)
async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(DishForm.price)
    await message.answer("Задайте цену блюда:")

@dish_router.message(DishForm.price)
async def process_dish_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(DishForm.category)
    await message.answer("Какую категорию имеет блюдо? (например, супы, вторые блюда, напитки)")

@dish_router.message(DishForm.category)
async def process_dish_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]
        ],
        resize_keyboard=True
    )

    await state.set_state(DishForm.confirm)
    await message.answer(f"Вы ввели:\nНазвание: {data['name']},\nЦена: {data['price']},\nКатегория: {data['category']}", reply_markup=kb)

@dish_router.message(DishForm.confirm, F.text == "Да")
async def process_dish_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()

    kb = types.ReplyKeyboardRemove()

    with sqlite3.connect(database) as connection:
        connection.execute("""
            INSERT INTO dishes (name, price, category)
            VALUES (?, ?, ?)
        """, (data['name'], data['price'], data['category']))

    await message.answer("Блюдо было добавлено в меню!", reply_markup=kb)
    await state.clear()

@dish_router.message(DishForm.confirm, F.text == "Нет")
async def process_dish_cancel(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await message.answer("Добавление блюда было отменено", reply_markup=kb)
    await state.clear()
