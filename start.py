from aiogram import Router, F, types
from aiogram.filters.command import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Наш адрес', 
                                           url='https://g.co/kgs/tv1eXkZ'),
                types.InlineKeyboardButton(text='Контакты', 
                                           callback_data='contacts')
            ],
            [
                types.InlineKeyboardButton(text='О нас', 
                                            callback_data='about_us'),  
                types.InlineKeyboardButton(text='Наш сайт',
                                            url='https://taplink.cc/capitokg?fbclid=PAZXh0bgNhZW0CMTEAAabzZ6_tnL4Zr9hr7LvfxOE_OAqlYs_GgyfoCBjw2IdnyHOCOTx_DLe_Y60_aem_GzKbDGsYw_JOIGCQ5fybtA')
            ],
            [
                types.InlineKeyboardButton(text='Instagram',
                                            url='https://www.instagram.com/capito.bishkek/'),
                types.InlineKeyboardButton(text='Отзывы',
                                            callback_data='feedback')
            ],
            [
                types.InlineKeyboardButton(text='Наши вакансии', 
                                           callback_data='vacancies')
            ]
        ]
    )
    await message.answer(f'Добро пожаловать в нашу кофейню, {user_id}! Выберите интересующую информацию:', reply_markup=kb)

@start_router.callback_query(F.data == 'contacts')
async def contacts_handler(callback: types.CallbackQuery):
    await callback.message.answer('Наши контакты: +996 998 100 724')
    await callback.answer()

@start_router.callback_query(F.data == 'about_us')  
async def about_us_handler(callback: types.CallbackQuery):
    await callback.message.answer('О нас: Мы - самая уютная кофейня в Бишкеке со множеством филиалов по всему городу')
    await callback.answer()

@start_router.callback_query(F.data == 'feedback')
async def feedback_handler(callback: types.CallbackQuery):
    await callback.message.answer("Спасибо за ваши отзывы! Оставить отзыв можно по ссылке: https://www.instagram.com/direct/t/100472214691218")
    await callback.answer()

@start_router.callback_query(F.data == 'vacancies')
async def vacancies_handler(callback: types.CallbackQuery):
    await callback.message.answer("У нас открыты вакансии! Контакты для связи: +996 755 318 888")
    await callback.answer()
