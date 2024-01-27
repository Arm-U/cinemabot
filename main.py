from aiogram import Bot, types, Dispatcher, executor  # type: ignore
from src import bot_impl
from src import database
from src import my_config


bot = Bot(my_config.CONFIG['TOKEN'])
dp = Dispatcher(bot)
db = database.DataBase()
tg_bot = bot_impl.TelegramBot(db)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await tg_bot.start_message(message)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await tg_bot.help_message(message)


@dp.message_handler(commands=['history'])
async def history_message(message: types.Message):
    await tg_bot.history_message(message)


@dp.message_handler(commands=['stats'])
async def stats_message(message: types.Message):
    await tg_bot.stats_message(message)


@dp.message_handler()
async def get_info(message: types.Message):
    await tg_bot.search_message(message)


if __name__ == '__main__':
    executor.start_polling(dp)
