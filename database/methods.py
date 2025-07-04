"""
Модуль database.methods

Содержит функции для выполнения операций с базой данных,
включая подключение, запросы и обработку результатов.
"""
from typing import Union, Dict, List
import logging  # Импортируем модуль для ведения журналов
from config_data.config import DATABASE_URL
from database.models import Database

db = Database(DATABASE_URL)
logger = logging.getLogger(__name__)


async def country_get(country: str) -> Union[Dict, str]:
    """
    Асинхронная функция.
    Получает запись из базы данных по названию страны.
    Args:
        country (str): Название страны
    Returns:
        Union[Dict, str]: Словарь с данными, если запись найдена
                          или сообщение об ошибке или отсутствии записи
    """
    try:
        record = await db.fetch_record_by_country(country)
        if record:
            return dict(record[0])
        return "Запись не найдена."
    except Exception as e:
        logger.error("Ошибка в обработчике: %s", e)
        raise


async def town_get_police(
        town: str,
        country: str
) -> Union[List[Dict], Dict]:
    """
    Асинхронная функция.
    Получает записи полиции по городу и стране.
    Args:
        town (str): Название города.
        country (str): Название страны.
    Returns:
        Union[List[Dict], Dict]: Список записей или сообщение об ошибке.
    """
    try:
        records = await db.fetch_record_by_town_police(town, country)
        list_of_dicts = [dict(record) for record in records]
        if list_of_dicts:
            return list_of_dicts
        return {"error": "Запись не найдена."}
    except Exception as e:
        logger.error("Ошибка в обработчике: %s", e)
        raise


async def town_get_hospital(
        town: str,
        country: str
) -> Union[List[Dict], Dict]:
    """
    Асинхронная функция.
    Получает записи больниц по городу и стране.
    Args:
        town (str): Название города.
        country (str): Название страны.
    Returns:
        Union[List[Dict], Dict]: Список записей или сообщение об ошибке.
    """
    try:
        records = await db.fetch_record_by_town_hospital(town, country)
        list_of_dicts = [dict(record) for record in records]
        if list_of_dicts:
            return list_of_dicts
        return {"error": "Запись не найдена."}
    except Exception as e:
        logger.error("Ошибка в обработчике: %s", e)
        raise


async def town_get_help_center(
        town: str,
        country: str
) -> Union[List[Dict], Dict]:
    """
    Асинхронная функция.
    Получает записи центров помощи по городу и стране.
    Args:
        town (str): Название города.
        country (str): Название страны.
    Returns:
        Union[List[Dict], Dict]: Список записей или сообщение об ошибке.
    """
    try:
        records = await db.fetch_record_by_town_help_center(town, country)
        list_of_dicts = [dict(record) for record in records]
        if list_of_dicts:
            return list_of_dicts
        return {"error": "Запись не найдена."}
    except Exception as e:
        logger.error("Ошибка в обработчике: %s", e)
        raise


async def on_startup():
    """
    Асинхронная функция, выполняющаяся при запуске бота.
    Подключается к базе данных и выводит информационное сообщение.
    """
    logger.info("🟢 Бот запускается...")
    await db.connect()


async def on_shutdown():
    """
    Асинхронная функция, выполняемая при остановке бота.
    Закрывает соединение с базой данных и выводит информационное сообщение.
    """
    logger.info("🔴 Бот останавливается...")
    await db.close()
