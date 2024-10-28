from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3
from bot_config import database

class ReviewForm(StatesGroup):
    name = State()
    rating = State()
    comment = State()
    confirm = State()

review_router = Router()

@review_router.message(Command("leave_review"))
async def start_review_form(message: types.Message, state: FSMContext):
    await state.set_state(ReviewForm.name)
    await message.answer("Как Вас зовут?")

@review_router.message(ReviewForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ReviewForm.rating)
    await message.answer("Какую оценку Вы ставите? (от 1 до 5)")

@review_router.message(ReviewForm.rating)
async def process_rating(message: types.Message, state: FSMContext):
    rating = int(message.text)
    if 1 <= rating <= 5:
        await state.update_data(rating=rating)
        await state.set_state(ReviewForm.comment)
        await message.answer("Ваш комментарий:")
    else:
        await message.answer("Пожалуйста, введите оценку от 1 до 5.")

@review_router.message(ReviewForm.comment)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]
        ],
        resize_keyboard=True
    )
    await state.set_state(ReviewForm.confirm)
    await message.answer(f"Вы ввели:\nИмя: {data['name']},\nОценка: {data['rating']},\nКомментарий: {data['comment']}", reply_markup=kb)

@review_router.message(ReviewForm.confirm, F.text == "Да")
async def process_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    with sqlite3.connect(database) as connection:
        connection.execute("""
            INSERT INTO reviews (name, rating, comment)
            VALUES (?, ?, ?)
        """, (data['name'], data['rating'], data['comment']))
    
    await message.answer("Ваш отзыв был сохранен!")
    await state.clear()

@review_router.message(ReviewForm.confirm, F.text == "Нет")
async def process_cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили оставление отзыва")
    await state.clear()