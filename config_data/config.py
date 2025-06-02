"""
Модуль config.py

Содержит настройки и конфигурационные данные для проекта.
"""
import os
from typing import Dict, Optional, Any
# импортируем декоратор, который упрощает создание классов
from dataclasses import dataclass

from dotenv import load_dotenv
import requests
# импортируем класс для работы с переменными окружения
from environs import Env

load_dotenv()  # Загружает переменные из .env файла

API_KEY = os.getenv("API_KEY")
KEY_TRANSLATE = os.getenv("API_KEY_TRANSLATE")
FOLDER_ID = os.getenv("FOLDER_ID")
# API геокодирования Яндекс
API_GEO = 'https://geocode-maps.yandex.ru/v1'
# API яндекс переводчика
API_TRANSLATE = "https://translate.api.cloud.yandex.net/translate/v2/translate"
# Адрес база данных POSTGRESQL
DATABASE_URL = os.getenv("DATABASE_URL")


@dataclass
class TgBot:
    """
    Класс, который хранит информацию о Telegram-боте.

    Attributes:
        token (str): Токен для доступа к Telegram-боту.
    """
    token: str


@dataclass
class Config:
    """
    Класс для хранения конфигурационных данных приложения.
    Attributes:
        tg_bot (TgBot): Экземпляр класса TgBot с настройками Telegram-бота.
    """
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    """
    Функция загружает конфигурацию из .env и возвращает заполненный экземпляр класса Config
    Args:
        path (str | None): Путь к файлу .env. Если None используется стандартный путь
    Returns:
        Config: Экземпляр класса Config с заполненными параметрами из .env
    """
    # Создаем объект класса для работы с переменными окружения
    env = Env()
    # Читаем переменные окружения
    env.read_env(path)
    # Создаем экземпляр класса
    return Config(
        # Передаем новый экземпляр класса
        tg_bot=TgBot(
            # Заполняем экземпляр класса значениями переменной окружения
            token=env('BOT_TOKEN')
        )
    )


def api_request(endpoint: str, params: Optional[dict[str, Any]] = None) -> requests.Response:
    """
    Функция выполняет GET-запрос к API с добавлением API-ключа в параметры
    Args:
        endpoint (str): URL конечной точки API
        params: (Optional[dict[str, Any]]): Словарь параметров запроса.
         Если None, создается пустой словарь
    Returns:
        requests.Response: Объект ответа от сервера
    """
    if params is None:
        params = {}
    params['apikey'] = API_KEY
    return requests.get(
        f'{endpoint}',
        params=params,
        timeout=10  # Таймаут в 10 секунд
    )


def get_coord(geocode: str, response_format: str = 'json', lang: str = 'ru_RU') -> Optional[Dict]:
    """
    Получает координаты по адресу с помощью геокодера.
    Args:
        geocode (str): Адрес или описание места для геокодирования.
        response_format (str): Формат ответа (по умолчанию 'json').
        lang (str): Язык ответа (по умолчанию 'ru_RU').
    Returns:
        Optional[Dict]: Распарсенный JSON-ответ с координатами или None при ошибке
    """
    response = api_request(f'{API_GEO}', params={
        'format': response_format,
        'geocode': geocode,
        'lang': lang,
    })
    response.raise_for_status()
    return response.json()


def translate_text(text: str, target_language: str) -> str:
    """
    Переводит текст на указанный язык с помощью Yandex Cloud Translate API.
    Args:
        text (str): Текст для перевода.
        target_language (str): Код целевого языка (например, 'ru', 'en')
    Returns:
         str: Переведенный текст или сообщение об ошибке.
    """
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    headers = {"Authorization": f"Bearer {KEY_TRANSLATE}"}
    data = {
        "folder_id": FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": target_language,
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()  # Проверка на ошибки HTTP
        result = response.json()
        if "translations" in result and len(result["translations"]) > 0:
            return result["translations"][0]["text"]
        print(f"Ошибка в ответе API: {result}")
        return "Ошибка перевода: Не удалось получить результат"
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return "Ошибка перевода: Проблемы с запросом"
    except KeyError as e:
        print(f"Ошибка ключа в ответе API: {e}")
        return "Ошибка перевода: Неверный формат ответа"
