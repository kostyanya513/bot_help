from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.methods import (town_get_police,
                              town_get_help_center,
                              town_get_hospital)
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
from database.models import (user_dict,
                             data_variable)
from utils.utils import (get_or_create_telegraph_token,
                         create_telegraph_article,
                         translate_text)


# Функция, генерирующая клавиатуру главного меню
def create_main_menu() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_MAIN_MENU.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру главного меню если пользователь не указал гео
def create_main_menu_not_geo() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_MAIN_MENU_NOT_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру возврата из панели ввода страны нахождения в главное меню
def create_return_to_main_menu() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_RETURN_TO_MAIN_MENU.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_geo_lacation() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text='Отправить свою геолокацию',
                            request_location=True)
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             keyboard=[[button]])
    return kb

# Функция, генерирующая клавиатуру запроса помощи
def create_need_help() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_NEED_HELP.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру выбора делиться гео или нет
def create_choose_shar_or_not() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_CHOOSE_SHAR_OR_NOT.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру возврата из панели геолокации в меню запроса геолокации
def create_return_to_not_share_geo() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_RETURN_TO_NOT_SHARE_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру возврата из панели геолокации в меню запроса геолокации по пути сразу к главному меню
def create_return_to_share_geo() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_RETURN_TO_SHARE_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру выбора находится ли пользователь в безопасности
def create_user_safe() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_USER_SAFE.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру перед тем, как он поделился геопозицией
def create_after_share_geo_bot() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_AFTER_METHOD_DETERMINING_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру после того, как он поделился геопозицией
def create_share_geo_bot() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_METHOD_DETERMINING_GEO.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру подтверждения введенных данных
def create_data_confirmation() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_DATA_CONFIRMATION.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Функция, генерирующая клавиатуру при отсутствии геоданных пользователя
def create_not_location() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_NOT_LOCATION.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру для выбора вида помощи пользователю
def create_choosing_type_help() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вызвать экстренную помощь",
                              callback_data="emergency_assistance")],
        [InlineKeyboardButton(text="Советы по уходу в безопасное место",
                              url="https://telegra.ph/Kak-ujti-v-bezopasnoe-mesto-04-07")],
        [InlineKeyboardButton(text="Техники самообороны",
                              url="https://telegra.ph/Tehniki-samooborony-04-07")],
        [InlineKeyboardButton(text="Манипуляции для защиты",
                              url="https://telegra.ph/Manipulyativnye-tehniki-dlya-obezvrezhivaniya-nasilnika-04-07")],
        [InlineKeyboardButton(text="Психологическая поддержка",
                              callback_data="psychological_support")],
        [InlineKeyboardButton(text="Я в безопасности",
                              callback_data="i_safe")],
    ])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder

# Функция, генерирующая клавиатуру поиска точек
def create_points() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_POINTS.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру поиска описания территории
def create_description_territory() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_DESCRIPTION_TERRITORY.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру отправной точки
def create_time_point_departure() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_CREATE_TIME_POINT_DEPARTURE.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру связи с экстренными службами
def create_contact_emergency_services() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_CONTACT_EMERGENCY_SERVICES.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру безопасности пользователя
def create_geo_confirmation() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_DATA_CONFIRMATION.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру подтверждения введенной информации
def create_information_verification() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_INFORMATION_VERIFICATION.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру корректировки информации
def create_correct_information() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_CORRECT_INFORMATION.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру необходимой помощи
def create_type_help() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_TYPE_HELP.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру для звонка в sos службы с телеграм
def create_phone_list() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад",
                              callback_data="not_call")],
        [InlineKeyboardButton(text="Это как?",
                              url="https://telegra.ph/Vsyo-o-sos-telefone-04-07")],
    ])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder

# Функция, генерирующая клавиатуру меню полиции
def create_need_police() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_NEED_POLICE.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру меню мед помощи
def create_need_medical_help() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_NEED_MEDICAL_HELP.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


# Функция, генерирующая клавиатуру меню центров помощи
async def create_all_centers(user_id, user_autor, user_title) -> InlineKeyboardMarkup:
    text_translate = translate_text(user_id, user_dict[user_id]['sity']).strip(' .')
    town_info_police = await town_get_police(text_translate)
    town_info_hospitals = await town_get_hospital(text_translate)
    town_info_help_center = await town_get_help_center(text_translate)
    title = (f'{LEXICON['all_places']}\n'
             f'Город: {user_dict[user_id]['sity']}')
    author = user_autor or "Автор"
    if town_info_police:
        content_police = [[f'Название: {town["name"]}\n'
                           f'Адрес: {town["address"]}\n'
                           f'Телефон: {town["phone"]}\n'] for town in town_info_police]
    if town_info_hospitals:
        content_hospitals = [[f'Название: {town['name']}\n'
                              f'Адрес: {town['address']}\n'
                              f'Телефон: {town['phone']}\n'
                              f'Описание: {town['description']}\n'
                              f'Почта: {town['email']}\n'
                              f'Сайт: {town['website']}\n'] for town in town_info_hospitals]
    if town_info_help_center:
        content_help_center = [[f'Организация: {town['organization']}\n'
                                f'Адрес: {town['address']}\n'
                                f'Описание: {town['description']}\n'
                                f'Телефон: {town['phone']}\n'
                                f'SOS телефон: {town['sos_phone']}\n'
                                f'Почта: {town['email']}\n'
                                f'Сайт: {town['website']}\n'] for town in town_info_help_center]

    res = sum((lst for lst in [content_police, content_hospitals, content_help_center] if lst), [])
    content = [{'tag': 'p', 'children': resul} for resul in res]
    access_token = await get_or_create_telegraph_token(user_id)
    url_telegraph = await create_telegraph_article(access_token, title, author, content)
    kb_builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{user_title}',
                              url=url_telegraph)],
        [InlineKeyboardButton(text="В главное меню",
                              callback_data="main_menu")],
    ])
    return kb_builder


# Функция, генерирующая клавиатуру списка переменных, указанных пользователем
def create_variables(from_id) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in user_dict[from_id].items():
        if text != 'country_cod':
            buttons.append(InlineKeyboardButton(
                text=data_variable[text],
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


# Функция, генерирующая клавиатуру НАЗАД в базу данных
def create_back_change() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_BACK_CHANGE.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

# Функция, генерирующая клавиатуру ввода или изменения указанных данных
def create_send_or_enter() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов
    for text, button in LEXICON_SEND_OR_ENTER.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=text
        ))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()