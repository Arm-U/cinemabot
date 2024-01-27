from aiogram import types  # type: ignore
import typing as tp
from .helper_classes import Film, LogItem
from .film_search import FilmSearch
from .database import DataBase
from datetime import datetime


start_text: str = """
Привет! 👋 Добро пожаловать в бот "Кино в большом городе"! 🎬

Этот бот предназначен для поиска информации о фильмах и сериалах.
Просто напиши название интересующего тебя кинопроизведения,
 и я постараюсь предоставить тебе нужную информацию.

Для получения списка команд в любой момент используй /help.
 Удачного просмотра! 🍿🎥
"""
help_text: str = """
🎥 Команды бота "Кино в большом городе" 🌆:

/start - Начать взаимодействие с ботом.
/help - Получить список доступных команд и их описание.
/history - Просмотреть историю поиска.
/stats - Получить статистику по истории поиска.

Для поиска информации о фильме или сериале просто напиши его название.
 Наслаждайся кино в большом городе! 🍿🎬
"""
search_text = """
🎬 Название: {}
⭐ Рейтинг: {}

📝 Описание: {}

📺 Ссылка для просмотра: {}

Наслаждайся просмотром! 🍿🎥
"""


class TelegramBot:
    def __init__(self, db: DataBase):
        self.search_engine = FilmSearch()
        self.db = db

    async def start_message(self, message: types.Message):
        await message.answer(start_text)

    async def help_message(self, message: types.Message):
        await message.answer(help_text)

    async def history_message(self, message: types.Message):
        res: tp.List[LogItem] = self.db.get_history(message.chat.id)
        text_list = [f'⏰ {log.search_time} --- {log.name}' for log in res]
        text = '\n'.join(text_list)
        if text == '':
            text = 'Извините, вы пока ничего не искали'
        text = 'История поиска:\n' + text
        await message.answer(text)

    async def stats_message(self, message: types.Message):
        res: tp.List[tp.Any] = self.db.get_stats(message.chat.id)
        text_list = [f'🎥 {log[0]} --- {log[1]} запросов' for log in res]
        text = '\n'.join(text_list)
        if text == '':
            text = 'Извините, вы пока ничего не искали'
        text = 'Статистика поиска:\n' + text
        await message.answer(text)

    async def search_message(self, message: types.Message):
        film: tp.Optional[Film] = await self.search_engine.search_film(message)
        if not film:
            await message.answer(
                'Извините, по вашему запросу ничего не нашлось'
            )
        else:
            text = search_text.format(
                film.name, film.rating, film.description, film.link
            )
            log = LogItem(message.chat.id, film.name, datetime.now())
            self.db.insert_log(log)
            await message.answer_photo(photo=film.poster, caption=text)
