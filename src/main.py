import asyncio
from aiogram import Bot, Dispatcher
from src.settings import settings
import logging
import sys
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.services.llm_service import LLM, get_llm_answer
from src.dao.dao import execute_sql
import re


dp = Dispatcher()
llm = LLM()


@dp.message(CommandStart())
async def start_handler(message: Message):
    '''
    Handle /start
    '''
    await message.answer('Пишите ваш вопрос насчет видео')


@dp.message()
async def main_handler(message: Message):
    '''
    Handle all others messages
    '''
    try:
        sql_query = get_llm_answer(llm, message.text)
        clear_sql = re.sub(r'\n', ' ', sql_query)
        record_list = await execute_sql(clear_sql[7:-3])
        record = record_list[0].values()
        answer = None
        for val in record:
            answer = str(val)
        await message.answer(answer)
    except Exception as e:
        logging.error(e)
        await message.answer('Видимо, что-то пошло не так')


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())