"""
Модуль other_handlers содержит обработчики сообщений
для дополнительных команд и событий бота.
"""
from typing import Optional

from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def send_echo(message: Message):
    """
    Отвечает на любые непредусмотренные сообщения пользователя.
    Args:
        message (Message): Входящее сообщение от пользователя.
    """
    text: Optional[str] = message.text or "<пустое сообщение>"
    await message.answer(f'Не разобрал команду! '
                         f'Повтори пожалуйста! {text}')
