import typing as tp

CONFIG: tp.Dict[str, tp.Any] = {
    'TOKEN': 'Telegram API token',
    'film_link': 'https://www.kinopoisk.gg/film/',
    'search_headers': {
        'X-API-KEY': 'kinopoiskapiunofficial API token',
        'Content-Type': 'application/json'
    },
    'search_link': 'https://kinopoiskapiunofficial.tech/api/v2.1/films/'
}
