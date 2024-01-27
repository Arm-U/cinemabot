from dataclasses import dataclass
from typing import Optional
from aiogram import types  # type: ignore
from datetime import datetime


@dataclass
class Film:
    name: Optional[str] = None
    rating: Optional[str] = None
    description: Optional[str] = None
    poster: Optional[str] = None
    link: Optional[str] = None


@dataclass
class LogItem:
    chat_id: types.base.Integer
    name: Optional[str]
    search_time: datetime
