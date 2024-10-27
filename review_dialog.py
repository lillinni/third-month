from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.message(Command('review'))
async def start_review(message: types.Message, state: FSMContext):
    await state.set_state(RestaurantReview.name)
    await message.answer('Как Вас зовут?')

@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    await message.answer('Пожалуйста, укажите Ваш номер телефона или Instagram (например, @username)')

@review_router.message(RestaurantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer('Когда Вы посещали наше заведение? Укажите дату')

@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='1'), types.KeyboardButton(text='2'), types.KeyboardButton(text='3'),
             types.KeyboardButton(text='4'), types.KeyboardButton(text='5')]
        ], 
        resize_keyboard=True
    )
    await state.set_state(RestaurantReview.food_rating)
    await message.answer('Оцените качество еды от 1 до 5:', reply_markup=kb)

@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='1'), types.KeyboardButton(text='2'), types.KeyboardButton(text='3'),
             types.KeyboardButton(text='4'), types.KeyboardButton(text='5')]
        ], 
        resize_keyboard=True
    )
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer('Оцените чистоту заведения от 1 до 5:', reply_markup=kb)

@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer('Если у Вас есть дополнительные комментарии или жалобы, напишите их ниже', 
                         reply_markup=types.ReplyKeyboardRemove())

@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()

    review_text = (
        f"Спасибо за Ваш отзыв, {data['name']}!\n\n"
        f"Контактная информация: {data['phone_number']}\n"
        f"Дата посещения: {data['visit_date']}\n"
        f"Оценка качества еды: {data['food_rating']}\n"
        f"Оценка чистоты: {data['cleanliness_rating']}\n"
        f"Дополнительные комментарии: {data['extra_comments']}"
    )

    await message.answer(review_text)
    await state.clear()
    await message.answer('Спасибо за Ваш отзыв!')
