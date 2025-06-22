"""
Модуль keyboards.set_menu

Содержит функции для создания клавиатур меню бота.
"""
from typing import Union
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import (user_dict,
                             data_variable)
from lexicon.lexicon_ru import (LEXICON_MAIN_MENU,
                                LEXICON_RETURN_TO_MAIN_MENU,
                                LEXICON_NEED_HELP,
                                LEXICON_CHOOSE_SHAR_OR_NOT,
                                LEXICON_RETURN_TO_NOT_SHARE_GEO,
                                LEXICON_RETURN_TO_SHARE_GEO,
                                LEXICON_USER_SAFE,
                                LEXICON_METHOD_DETERMINING_GEO,
                                LEXICON_DATA_CONFIRMATION,
                                LEXICON_NOT_LOCATION,
                                LEXICON_POINTS,
                                LEXICON_DESCRIPTION_TERRITORY,
                                LEXICON_CREATE_TIME_POINT_DEPARTURE,
                                LEXICON_CONTACT_EMERGENCY_SERVICES,
                                LEXICON_INFORMATION_VERIFICATION,
                                LEXICON_CORRECT_INFORMATION,
                                LEXICON_TYPE_HELP,
                                LEXICON_NEED_POLICE,
                                LEXICON_NEED_MEDICAL_HELP,
                                LEXICON_BACK_CHANGE,
                                LEXICON_AFTER_METHOD_DETERMINING_GEO,
                                LEXICON_SEND_OR_ENTER,
                                LEXICON_MAIN_MENU_NOT_GEO,
                                LEXICON)
from utils.utils import (get_user_location_data,
                         get_translated_city,
                         get_centers_data,
                         build_telegraph_content,
                         create_telegraph_article_for_centers,
                         get_translated_country)


def create_main_menu() -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру главного меню с кнопками из словаря
    LEXICON_MAIN_MENU.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        главного меню.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_MAIN_MENU.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_main_menu_not_geo() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру главного меню для пользователей,
    которые не указали геолокацию.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        главного меню без гео.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_MAIN_MENU_NOT_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_return_to_main_menu() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками для возврата из панели ввода страны
    нахождения в главное меню.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками возврата
        в главное меню.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_RETURN_TO_MAIN_MENU.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_geo_location() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопкой для отправки геолокации пользователя.
    Returns:
        ReplyKeyboardMarkup: Объект клавиатуры с кнопкой запроса геолокации.
    """
    button = KeyboardButton(
        text='Отправить свою геолокацию',
        request_location=True
    )
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[button]]
    )
    return kb


def create_need_help() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками запроса помощи из словаря
    LEXICON_NEED_HELP.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками помощи.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_NEED_HELP.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Функция, генерирующая клавиатуру выбора делиться гео или нет
def create_choose_shar_or_not() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора, делиться геолокацией или нет,
    используя словарь LEXICON_CHOOSE_SHAR_OR_NOT.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками выбора.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_CHOOSE_SHAR_OR_NOT.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_return_to_not_share_geo() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для возврата из панели отказа от
    предоставления геолокации в меню запроса геолокации.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками возврата.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_RETURN_TO_NOT_SHARE_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_return_to_share_geo() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для возврата из панели геолокации в меню
    запроса геолокации, с возможностью сразу перейти в главное меню.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками возврата.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_RETURN_TO_SHARE_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_user_safe() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора, находится ли пользователь
    в безопасности, используя словарь LEXICON_USER_SAFE.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        выбора безопасности пользователя.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_USER_SAFE.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_after_share_geo_bot() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру, отображаемую после того, как пользователь
    поделился геопозицией, используя словарь
    LEXICON_AFTER_METHOD_DETERMINING_GEO.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с соответствующими
        кнопками.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in (
            LEXICON_AFTER_METHOD_DETERMINING_GEO.items()
    ):
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_share_geo_bot() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру, отображаемую после того, как пользователь
    поделился геопозицией, используя словарь LEXICON_METHOD_DETERMINING_GEO.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с соответствующими
        кнопками.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_METHOD_DETERMINING_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_data_confirmation() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для подтверждения введённых пользователем
    данных, используя словарь LEXICON_DATA_CONFIRMATION.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        подтверждения данных.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_DATA_CONFIRMATION.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_not_location() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру, отображаемую при отсутствии
    геоданных пользователя,
    используя словарь LEXICON_NOT_LOCATION.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        для обработки отсутствия геоданных.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_NOT_LOCATION.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_choosing_type_help() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора вида помощи пользователю.
    Содержит кнопки с callback_data и ссылки на полезные ресурсы.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с вариантами помощи.
    """
    kb_builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вызвать экстренную помощь",
                              callback_data="emergency_assistance")],
        [InlineKeyboardButton(text="Советы по уходу в безопасное место",
                              url=(
                                  "https://telegra.ph/"
                                  "Kak-ujti-v-bezopasnoe-mesto-04-07"
                              ))],
        [InlineKeyboardButton(text="Техники самообороны",
                              url=(
                                  "https://telegra.ph/"
                                  "Tehniki-samooborony-04-07"
                              ))],
        [InlineKeyboardButton(text="Манипуляции для защиты",
                              url=(
                                  "https://telegra.ph/Manipulyativnye-tehniki-"
                                  "dlya-obezvrezhivaniya-nasilnika-04-07"
                              ))],
        [InlineKeyboardButton(text="Психологическая поддержка",
                              callback_data="psychological_support")],
        [InlineKeyboardButton(text="Я в безопасности",
                              callback_data="i_safe")],
    ])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder


def create_points() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для поиска точек, используя словарь
    LEXICON_POINTS.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        для выбора точек.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_POINTS.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_description_territory() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора описания территории,
    используя словарь LEXICON_DESCRIPTION_TERRITORY.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        описания территории.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_DESCRIPTION_TERRITORY.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_time_point_departure() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора отправной точки,
    используя словарь LEXICON_CREATE_TIME_POINT_DEPARTURE.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        выбора отправной точки.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in (
            LEXICON_CREATE_TIME_POINT_DEPARTURE.items()
    ):
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_contact_emergency_services() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для связи с экстренными службами,
    используя словарь LEXICON_CONTACT_EMERGENCY_SERVICES.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        связи с экстренными службами.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in (
            LEXICON_CONTACT_EMERGENCY_SERVICES.items()
    ):
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_geo_confirmation() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для подтверждения безопасности пользователя,
    используя словарь LEXICON_DATA_CONFIRMATION.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        подтверждения безопасности.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_DATA_CONFIRMATION.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_information_verification() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для подтверждения введённой информации,
    используя словарь LEXICON_INFORMATION_VERIFICATION.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        подтверждения информации.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_INFORMATION_VERIFICATION.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Функция, генерирующая клавиатуру корректировки информации
def create_correct_information() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для корректировки информации,
    используя словарь LEXICON_CORRECT_INFORMATION.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        корректировки информации.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_CORRECT_INFORMATION.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_type_help() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора типа необходимой помощи,
    используя словарь LEXICON_TYPE_HELP.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        выбора типа помощи.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_TYPE_HELP.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_phone_list() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для звонка в SOS службы с кнопками:
    - "Назад" с callback_data для возврата
    - "Это как?" со ссылкой на инструкцию по SOS телефону
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        звонка в SOS службы.
    """
    kb_builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад",
                              callback_data="not_call")],
        [InlineKeyboardButton(text="Это как?",
                              url=(
                                  "https://telegra.ph/"
                                  "Vsyo-o-sos-telefone-04-07"
                              ))],
    ])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder


def create_need_police() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру меню полиции,
    используя словарь LEXICON_NEED_POLICE.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками меню полиции.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_NEED_POLICE.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_need_medical_help() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру меню медицинской помощи,
    используя словарь LEXICON_NEED_MEDICAL_HELP.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        меню медицинской помощи.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_NEED_MEDICAL_HELP.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


async def create_all_centers(
        user_id: int,
        user_author: str,
        user_title: str
) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с ссылкой на статью Telegraph,
    содержащую информацию о центрах помощи
    (полиция, больницы, центры помощи) по городу пользователя.
    Args:
        user_id (int): ID пользователя.
        user_author (str): Автор статьи.
        user_title (str): Заголовок статьи (текст кнопки).
    Returns:
        InlineKeyboardMarkup: Инлайн-клавиатура с кнопками.
    """
    city_name, country_name = get_user_location_data(user_id=user_id)
    # Переводим название города
    city_translated = await get_translated_city(user_id=user_id)
    country_name = await get_translated_country(user_id=user_id)
    town = ''.join(city_translated.split(' ')[1:])
    country = ''.join(country_name.split(' ')[1:])
    police, hospitals, help_centers = await get_centers_data(
        city_translated=town,
        country=country
    )
    # Формируем заголовок статьи
    title = f"{LEXICON['all_places']}\nГород: {city_name}"
    author = user_author or "Автор"
    # Формируем структуру для Telegraph API
    content = build_telegraph_content(
        police=police,
        hospitals=hospitals,
        help_centers=help_centers
    )
    # Создаём статью
    url_telegraph = await create_telegraph_article_for_centers(
        user_id=user_id,
        title=title,
        author=author,
        content=content
    )
    # Создаём инлайн-клавиатуру с кнопкой на статью и возвратом в меню
    kb_builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{user_title}',
                              url=url_telegraph)],
        [InlineKeyboardButton(text="В главное меню",
                              callback_data="main_menu")],
    ])
    return kb_builder


def create_variables(from_id: Union[int, str]) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру списка переменных, указанных пользователем.
    Args:
        from_id (int | str): Идентификатор пользователя, по которому
        берутся данные из user_dict.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками
        переменных и кнопкой "Главное меню".
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    user_data = user_dict.get(from_id, {})
    for text, _ in user_data.items():
        if text != 'country_cod':
            buttons.append(InlineKeyboardButton(
                text=data_variable.get(text, text),
                callback_data=text
            ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    kb_builder.row(InlineKeyboardButton(
            text='Главное меню',
            callback_data='return_main_menu'
        ))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_back_change() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для кнопки "НАЗАД" в базу данных,
    используя словарь LEXICON_BACK_CHANGE.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками возврата.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_BACK_CHANGE.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_send_or_enter() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для выбора действия — отправить или ввести
    данные, используя словарь LEXICON_SEND_OR_ENTER.
    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками выбора
        действия.
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for callback_data, button_text in LEXICON_SEND_OR_ENTER.items():
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
