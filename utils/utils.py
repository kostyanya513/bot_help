"""
Модуль utils содержит вспомогательные функции для работы с переводами,
Telegraph API и обработкой данных пользователей.

Здесь реализованы функции для перевода текста, создания статей на Telegraph,
а также получения и обработки данных пользователей.
"""
from typing import (Union,
                    List,
                    Dict,
                    Optional,
                    Any,
                    Tuple)

from telegraph import Telegraph
from mymemopy.translator import MyMemoryTranslate

from config_data.config import translate_text
from database.methods import (town_get_police,
                              town_get_hospital,
                              town_get_help_center,
                              translate_country_cod,)
from database.models import (user_dict,
                             user_tokens)


# Инициализация переводчика (анонимный пользователь)
translator = MyMemoryTranslate()


async def translate_country(user_id: int, text: str):
    """
    Переводит название страны на английский язык.
    Args:
        user_id (int): Идентификатор пользователя.
        text (str): Название страны на исходном языке.
    Returns:
        str: Переведённый текст или сообщение об ошибке.
    """
    try:
        source_lang = user_dict[user_id]['country_cod']
        target_lang = 'en'
        translation = await translate_text(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang
        )
        return translation
    except KeyError:
        return "Ошибка: неверный user_id или отсутствует код страны."
    except Exception as e:
        return f"Ошибка перевода: {e}"


# Функция для перевода текста на язык пользователя
async def translate_town(user_id: int, town: str, country: str):
    """
    Переводит текст на язык пользователя.
    Args:
        user_id (int): Идентификатор пользователя.
        town (str): Город на языке пользователя.
    Returns:
        str: Переведённый текст или сообщение об ошибке.
    """
    try:
        source_lang = user_dict[user_id]['country_cod']  # Язык пользователя
        target_lang = await translate_country_cod(country)  # Язык, на который нужно перевести текст
        target_lang = target_lang[0]['country_code']
        if target_lang == source_lang:
            # Если язык пользователя совпадает с целевым (русским),
            # возвращаем с добавлением "Town"
            return town
        translation = await translate_text(
            text=town,
            source_lang=source_lang,
            target_lang=target_lang
        )
        return translation
    except KeyError:
        return "Ошибка: неверный user_id или отсутствует код страны."
    except Exception as e:
        return f"Ошибка перевода: {e}"


async def get_translated_city(user_id: int) -> str:
    """
    Получает название города пользователя и переводит его.
    Args:
        user_id (int): ID пользователя.
    Returns:
        str: Переведённое название города без пробелов и точек в конце.
    """
    city_name, country_name = await get_user_location_data(user_id)
    res = await translate_town(user_id, city_name, country_name)
    return res


async def get_translated_country(user_id: int) -> str:
    """
    Получает название страны пользователя и переводит его.
    Args:
        user_id (int): ID пользователя.
    Returns:
        str: Переведённое название страны без пробелов и точек в конце.
    """
    _, country_name = await get_user_location_data(user_id)
    res = (await translate_country(user_id, country_name)).strip(' .')
    return res


async def get_or_create_telegraph_token(user_id: int) -> str:
    """
    Получает или создаёт access_token для пользователя.
    В реальном приложении сохраняйте токен в БД.
    """
    if user_id in user_tokens:
        return user_tokens[user_id]
    telegraph = Telegraph()
    response = telegraph.create_account(short_name=f"user_{user_id}")
    access_token = response['access_token']
    user_tokens[user_id] = access_token
    return access_token


async def create_telegraph_article(
        access_token: str,
        title: str,
        author: str,
        content: list
) -> str:
    """
    Создает страницу на Telegraph и возвращает ссылку на неё.
    Args:
        access_token (str): Токен доступа пользователя Telegraph.
        title (str): Заголовок статьи.
        author (str): Имя автора статьи.
        content (list): Содержимое статьи в формате, поддерживаемом
        Telegraph API.
    Returns:
        str: URL созданной страницы на Telegraph.
    """
    telegraph = Telegraph(access_token=access_token)
    response = telegraph.create_page(title=title,
                                     author_name=author,
                                     content=content)
    return response['url']


def build_telegraph_content(
        police: Optional[List[Dict]],
        hospitals: Optional[List[Dict]],
        help_centers: Optional[List[Dict]]
) -> List[Dict[str, Any]]:
    """
    Объединяет и форматирует данные центров помощи в структуру для
    Telegraph API.
    Args:
        police (Optional[List[Dict]]): Данные полиции.
        hospitals (Optional[List[Dict]]): Данные больниц.
        help_centers (Optional[List[Dict]]): Данные центров помощи.
    Returns:
        List[Dict[str, Any]]: Список блоков контента для Telegraph.
    """
    content_police = (format_police_content(police)
                      if police
                      else [])
    content_hospitals = (format_hospitals_content(hospitals)
                         if hospitals
                         else [])
    content_help_center = (format_help_center_content(help_centers)
                           if help_centers
                           else [])
    combined = sum((lst for lst in [
        content_police,
        content_hospitals,
        content_help_center
    ] if lst), [])
    return [{'tag': 'p', 'children': item} for item in combined]


async def get_centers_data(
        city_translated: str,
        country: Optional[str]
) -> Tuple[
    Union[List[Dict], Dict],
    Union[List[Dict], Dict],
    Union[List[Dict], Dict]
]:
    """
    Асинхронно получает данные о центрах помощи: полиции, больницах
    и центрах помощи.
    Args:
        city_translated (str): Переведённое название города.
        country (Optional[str]): Название страны или None.
    Returns:
        Tuple[Union[List[Dict], Dict], Union[List[Dict], Dict],
        Union[List[Dict], Dict]]:
            Кортеж с тремя элементами — данные полиции, больниц
            и центров помощи.
    """
    police = await town_get_police(city_translated, country)
    hospitals = await town_get_hospital(city_translated, country)
    help_centers = await town_get_help_center(city_translated, country)
    return police, hospitals, help_centers


async def get_user_location_data(user_id: int) -> tuple[str, str | None]:
    city_name = user_dict[user_id]['sity']
    country_name = await translate_country(user_id, user_dict[user_id].get('country', None))
    return city_name, country_name


async def create_telegraph_article_for_centers(
        user_id: int,
        title: str,
        author: str,
        content: list
) -> str:
    """
    Асинхронно создаёт статью на Telegraph и возвращает URL.
    Args:
        user_id (int): ID пользователя.
        title (str): Заголовок статьи.
        author (str): Автор статьи.
        content (list): Контент статьи в формате Telegraph API.
    Returns:
        str: URL созданной статьи.
    """
    access_token = await get_or_create_telegraph_token(user_id)
    url = await create_telegraph_article(access_token, title, author, content)
    return url


def format_police_content(town_info_police: List[Dict]) -> List[List[str]]:
    """
    Форматирует список записей полиции в список списков строк для отображения.
    Args:
        town_info_police (List[Dict]): Список словарей с информацией о полиции.
    Returns:
        List[List[str]]: Список списков с форматированными строками.
    """
    return [
        [f"Название: {town['name']}\n"
         f"Адрес: {town['address']}\n"
         f"Телефон: {town['phone']}\n"]
        for town in town_info_police
    ]


def format_hospitals_content(
        town_info_hospitals: List[Dict]
) -> List[List[str]]:
    """
    Форматирует список записей больниц в список списков строк
    для отображения.
    Args:
        town_info_hospitals (List[Dict]): Список словарей с
        информацией о больницах.
    Returns:
        List[List[str]]: Список списков с форматированными строками.
    """
    return [
        [f"Название: {town['name']}\n"
         f"Адрес: {town['address']}\n"
         f"Телефон: {town['phone']}\n"
         f"Описание: {town['description']}\n"
         f"Почта: {town['email']}\n"
         f"Сайт: {town['website']}\n"]
        for town in town_info_hospitals
    ]


def format_help_center_content(
        town_info_help_center: List[Dict]
) -> List[List[str]]:
    """
    Форматирует список записей центров помощи в список списков
    строк для отображения.
    Args:
        town_info_help_center (List[Dict]): Список словарей с
        информацией о центрах помощи.
    Returns:
        List[List[str]]: Список списков с форматированными строками.
    """
    return [
        [f"Организация: {town['organization']}\n"
         f"Адрес: {town['address']}\n"
         f"Описание: {town['description']}\n"
         f"Телефон: {town['phone']}\n"
         f"SOS телефон: {town['sos_phone']}\n"
         f"Почта: {town['email']}\n"
         f"Сайт: {town['website']}\n"]
        for town in town_info_help_center
    ]
