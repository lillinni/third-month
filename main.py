# main.py
import asyncio 
import logging 

from bot_config import bot, dp
from handlers.start import start_router



async def main():
    dp.include_router(start_router)
    await dp.start_polling(bot) #zapusk bota

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


