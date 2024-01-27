import aiohttp
import json
from aiogram import types  # type: ignore
from .helper_classes import Film
from .my_config import CONFIG
import typing as tp


class FilmSearch:
    def __init__(self) -> None:
        self.search_link = CONFIG['search_link']
        self.headers = CONFIG['search_headers']
        self.default_photo: str = 'https://cdn-icons-png.flaticon.com'\
                                  '/512/4054/4054617.png'

    async def search_film(self, message: types.Message) -> tp.Optional[Film]:
        query: str = (self.search_link
                      + 'search-by-keyword?keyword='
                      + message.text + '&page=1')
        film: Film = Film()
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(query) as response:
                    if response.status == 200:
                        body = json.loads(await response.text())
                        film_data = body['films'][0]
                        film.name = film_data.get('nameRu', None)
                        film.rating = film_data.get(
                            'rating', 'Отсутствует рейтинг 😔'
                        )
                        film.description = film_data.get(
                            'description', 'Описание фильма отсутстует 😔'
                        )
                        film.poster = film_data.get(
                            'posterUrl', self.default_photo
                        )
                        id = film_data.get('filmId', None)
                        if id:
                            film.link = CONFIG['film_link'] + str(id)
        except Exception as e:
            print('Exception occured: ', e)

        return film if film.name else None
