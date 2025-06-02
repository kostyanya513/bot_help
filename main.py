"""
Основной модуль приложения.
Содержит обработчики команд и функции для работы с Telegram API.
"""
import asyncio  # Импортируем библиотеку для работы с асинхронным
# программированием
import logging  # Импортируем модуль для ведения журналов
from aiogram import (Bot, Dispatcher)  # Импортируем Bot, класс
# представляющий самого бота; # Dispatcher - класс, который управляет
# обработкой входящих обновлений
from aiogram.client.default import DefaultBotProperties  # Класс, который
# позволяет задать стандартные свойства бота
from aiogram.enums import ParseMode  # Перечисление, которое определяет режим
# парсинга текста

from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from config_data.config import Config, load_config
from database.methods import on_startup, on_shutdown

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    """
    Функция конфигурирования и запуска бота.
    """
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')  # Формат логирования

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Подключаем базу данных PostgreSQL
    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
