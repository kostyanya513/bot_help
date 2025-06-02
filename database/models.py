# Создаем "базу данных" пользователей
import asyncpg

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
                                 'safety': 'Безопасность',}

# Хранение access_token в памяти (для примера)
user_tokens: dict[int, str] = {}


class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(dsn=self.dsn)
            print("✅ Подключение к базе данных успешно установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения к базе: {e}")

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("✅ Подключение к базе данных закрыто")

    async def fetch_record_by_country(self, country_id):
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(f"SELECT * FROM sos_phones WHERE LOWER(country) = LOWER($1);", country_id)
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None

    async def fetch_record_by_town_police(self, town_id, country_id):
        table_name = f'police_{country_id.lower()}'
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(f"SELECT * FROM {table_name} WHERE LOWER(city) = LOWER($1);", town_id)
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None

    async def fetch_record_by_town_hospital(self, town_id, country_id):
        table_name = f'hospital_{country_id.lower()}'
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(f"SELECT * FROM {table_name} WHERE LOWER(city) = LOWER($1);", town_id)
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None

    async def fetch_record_by_town_help_center(self, town_id, country_id):
        table_name = f'help_center_{country_id.lower()}'
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(f"SELECT * FROM {table_name} WHERE LOWER(city) = LOWER($1);", town_id)
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return None
