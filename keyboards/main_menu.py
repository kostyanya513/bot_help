"""
Модуль main_menu содержит клавиатуру главного меню для Telegram-бота.
"""
from aiogram import Bot
from aiogram.types import BotCommand
from typing import List

from lexicon.lexicon_ru import LEXICON_COMMANDS


async def set_main_menu(bot: Bot) -> None:
    """
    Настраивает главное меню бота, устанавливая команды из LEXICON_COMMANDS.

    Args:
        bot (Bot): Экземпляр бота aiogram.
    """
    main_menu_commands: List[BotCommand] = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
