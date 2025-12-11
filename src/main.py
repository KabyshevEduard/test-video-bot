import asyncio
from aiogram import Bot, Dispatcher
from src.settings import settings
import logging
import sys
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.services.llm_service import LLM, get_llm_answer
#


dp = Dispatcher()
llm = LLM()


@dp.message(CommandStart())
async def start_handler(message: Message):
    '''
    Handle /start
    '''
    await message.answer('Пишите ваш вопрос')


@dp.message()
async def main_handler(message: Message):
    '''
    Handle all others messages
    '''
    #sql_query = get_llm_answer(message.text)
    await message.answer('Хороший вопрос')


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())