"""
Модуль models содержит классы и функции для работы с базой данных.
"""
from typing import Optional, List

import asyncpg  # type: ignore

from states.states import FSMFillForm

user_dict: dict[int, dict[str, str | int | bool]] = {}

# Создаем словарь переменных
data_variable: dict[str, str] = {'sity': 'Город',
                                 'country': 'Страна',
                                 'latitude': 'Широта',
                                 'longitude': 'Долгота',
                                 'info': 'Информация',
                                 'psyinput': 'Психоэмоциональное состояние',
                                 'legalreason': 'Легальность',
                                 'policeinput': 'Помощь полиции',
                                 'medinput': 'Мед помощь',
                                 'country_cod': 'Код страны',
                                 'safety': 'Безопасность'}

# Хранение access_token в памяти (для примера)
user_tokens: dict[int, str] = {}

# Маппинг для смены полей
CHANGE_FIELDS: dict[str, dict[str, str]] = {
    'sity': {
        'state': FSMFillForm.fill_change_sity,
        'lexicon': 'enter_new_value_sity',
        'key': 'sity',
    },
    'country': {
        'state': FSMFillForm.fill_change_country,
        'lexicon': 'enter_new_value_country',
        'key': 'country',
    },
    'latitude': {
        'state': FSMFillForm.fill_change_latitude,
        'lexicon': 'enter_new_value_latitude',
        'key': 'latitude',
    },
    'longitude': {
        'state': FSMFillForm.fill_change_longitude,
        'lexicon': 'enter_new_value_longitude',
        'key': 'longitude',
    },
    'info': {
        'state': FSMFillForm.fill_change_info,
        'lexicon': 'enter_new_value_info',
        'key': 'info',
    },
    'psyinput': {
        'state': FSMFillForm.fill_change_psyinput,
        'lexicon': 'enter_new_value_psyinput',
        'key': 'psyinput',
    },
    'legalreason': {
        'state': FSMFillForm.fill_change_legalreason,
        'lexicon': 'enter_new_value_legalreason',
        'key': 'legalreason',
    },
    'policeinput': {
        'state': FSMFillForm.fill_change_policeinput,
        'lexicon': 'enter_new_value_policeinput',
        'key': 'policeinput',
    },
    'medinput': {
        'state': FSMFillForm.fill_change_medinput,
        'lexicon': 'enter_new_value_medinput',
        'key': 'medinput',
    },
    'safety': {
        'state': FSMFillForm.fill_change_safety,
        'lexicon': 'enter_new_value_safety',
        'key': 'safety',
    },
}


class Database:
    """
    Класс для работы с базой данных
    Args:
        dsn (str): Строка подключения к базе данных.
    """
    def __init__(self, dsn: str) -> None:
        self.dsn: str = dsn
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """
        Создает пул соединений с базой данных.
        """
        try:
            self.pool = await asyncpg.create_pool(dsn=self.dsn)
            print("✅ Подключение к базе данных успешно установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения к базе: {e}")

    async def close(self) -> None:
        """
        Закрывает пул соединений.
        """
        if self.pool:
            await self.pool.close()
            print("✅ Подключение к базе данных закрыто")

    async def fetch_record_by_country(
            self,
            country_id: str
    ) -> Optional[List[asyncpg.Record]]:
        """
        Получить записи из таблицы sos_phones по названию страны
        Args:
            country_id (str): Название страны.
        Returns:
            Список записей или None в случае ошибки.
        """
        if not self.pool:
            print('❌ Пул соединений не инициализирован')
            return None
        try:
            async with self.pool.acquire() as conn:
                query = ("SELECT * FROM sos_phones"
                         " WHERE LOWER(country) = LOWER($1);")
                records = await conn.fetch(query, country_id)
                return records
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None

    async def fetch_record_by_town(self,
                                   town_id: str,
                                   country_id: str,
                                   service_type: str
                                   ) -> Optional[List[asyncpg.Record]]:
        """
        Получить записи из таблиц police, hospital
        или help_center по городу и стране.
        Args:
            town_id (str): Название города.
            country_id (str): Название страны.
            service_type (str): Тип сервиса
                                ('police', 'hospital', 'help_center').
        Returns:
            Список записей или None в случае ошибки.
        """
        if not self.pool:
            print("❌ Пул соединений не инициализирован")
            return None

        allowed_services = {'police', 'hospital', 'help_center'}
        if service_type not in allowed_services:
            print(f"❌ Недопустимый тип сервиса: {service_type}")
            return None

        table_name = f"{service_type}_{country_id.lower()}"

        try:
            async with self.pool.acquire() as conn:
                # В asyncpg нельзя параметризовать имена таблиц,
                # поэтому проверяем service_type заранее
                query = (f"SELECT * FROM {table_name}"
                         f" WHERE LOWER(city) = LOWER($1);")
                records = await conn.fetch(query, town_id)
                return records
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None

    async def fetch_record_by_town_police(
            self,
            town_id: str,
            country_id: str
    ) -> Optional[List[asyncpg.Record]]:
        """
            Получить записи полиции по городу и стране.

            Args:
                town_id (str): Название города.
                country_id (str): Название страны.

            Returns:
                Optional[List[asyncpg.Record]]: Список записей
                или None при ошибке.
            """
        return await self.fetch_record_by_town(town_id,
                                               country_id,
                                               'police')

    async def fetch_record_by_town_hospital(
            self,
            town_id: str,
            country_id: str
    ) -> Optional[List[asyncpg.Record]]:
        """
            Получить записи больниц по городу и стране.

            Args:
                town_id (str): Название города.
                country_id (str): Название страны.

            Returns:
                Optional[List[asyncpg.Record]]: Список записей
                или None при ошибке.
            """
        return await self.fetch_record_by_town(town_id,
                                               country_id,
                                               'hospital')

    async def fetch_record_by_town_help_center(
            self,
            town_id: str,
            country_id: str
    ) -> Optional[List[asyncpg.Record]]:
        """
            Получить записи центров помощи по городу и стране.

            Args:
                town_id (str): Название города.
                country_id (str): Название страны.

            Returns:
                Optional[List[asyncpg.Record]]: Список записей
                или None при ошибке.
            """
        return await self.fetch_record_by_town(town_id,
                                               country_id,
                                               'help_center')
