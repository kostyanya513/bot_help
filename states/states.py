"""
Модуль states.py содержит описание состояний конечного автомата (FSM)
для Telegram-бота, реализованного с помощью библиотеки aiogram.

В данном модуле определён класс FSMFillForm, который включает все состояния,
используемые для управления диалогом с пользователем.
"""
from aiogram.fsm.state import (StatesGroup,
                               State)


class FSMFillForm(StatesGroup):  # pylint: disable=too-few-public-methods
    """
    Класс FSMFillForm описывает все состояния конечного автомата (FSM) для
    взаимодействия пользователя с ботом. Каждое состояние соответствует
    определённому этапу диалога, в котором бот ожидает ввод или действие
    от пользователя.
    Состояния включают:
    - fill_country: ожидание ввода страны при старте бота
    - fill_town: ожидание ввода города
    - fill_need_help: выбор, нужна ли помощь
    - fill_shar_geo: запрос доступа к геолокации
    - fill_enter_geo: ожидание получения геопозиции
    - fill_enter_geo_main_menu: получение геопозиции из главного меню
    - fill_shar_geo_main_menu: запрос геолокации из главного меню
    - fill_return_shar_geo_main_menu: запрос возврата из уточнения гео
    в главное меню
    - fill_user_safe: запрос о безопасности пользователя
    - fill_user_share_geo_bot: подтверждение помощи через геолокацию
    - fill_return_shar_geo_clip: ожидание геопозиции из меню "СКРЕПКА"
    - fill_user_share_geo_bot_map: ожидание включения геолокации
    - fill_choosing_type_help: выбор вида помощи
    - fill_points_wifi_bluetooth: ввод точек WiFi и Bluetooth
    - fill_description_territory: ввод описания территории
    - fill_time_point_departure: ввод описания отправных данных
    - fill_contact_emergency_services: ожидание связи с экстренными службами
    - fill_security_confirmation: подтверждение безопасности после
    определения гео
    - fill_information_verification: подтверждение введённой информации
    - fill_correct_information: корректировка информации
    - fill_phone_list: выбор звонка из Telegram
    - fill_need_police: выбор действия в меню полиции
    - fill_need_medical_help: выбор действия в меню медпомощи
    - fill_legal_assistance: ввод основания в меню юридической помощи
    - fill_psycholog_support: ввод описания психического состояния
    - fill_help_centers: выбор действия в меню центров помощи
    - fill_all_police_stations: выбор действия в меню всех участков полиции
    - fill_your_question_police: ввод вопроса в меню полиции
    - fill_your_question_medical: ввод вопроса в меню медпомощи
    - fill_all_medical_center: выбор действия в меню всех медцентров
    - fill_change_sity: изменение города пользователя
    - fill_change_country: изменение страны пользователя
    - fill_change_latitude: изменение широты
    - fill_change_longitude: изменение долготы
    - fill_change_info: изменение информации о месте пребывания
    - fill_change_psyinput: изменение информации о состоянии пользователя
    - fill_change_legalreason: изменение информации о легальности пользователя
    - fill_change_policeinput: изменение вопроса полиции
    - fill_change_medinput: изменение вопроса медчасти
    - fill_change_safety: изменение вопроса безопасности пользователя
    - fill_correct_psychological_support: корректура психологического состояния
    - fill_phone_list_return_main: просмотр SOS телефонов или возврат
    в главное меню

    Этот класс позволяет гибко управлять логикой диалогов и переходами
    между состояниями в рамках бота на aiogram с использованием FSM.
    """
    fill_country = State()
    fill_town = State()
    fill_need_help = State()
    fill_shar_geo = State()
    fill_enter_geo = State()
    fill_enter_geo_main_menu = State()
    fill_shar_geo_main_menu = State()
    fill_return_shar_geo_main_menu = State()
    fill_user_safe = State()
    fill_user_share_geo_bot = State()
    fill_return_shar_geo_clip = State()
    fill_user_share_geo_bot_map = State()
    fill_choosing_type_help = State()
    fill_points_wifi_bluetooth = State()
    fill_description_territory = State()
    fill_time_point_departure = State()
    fill_contact_emergency_services = State()
    fill_security_confirmation = State()
    fill_information_verification = State()
    fill_correct_information = State()
    fill_phone_list = State()
    fill_need_police = State()
    fill_need_medical_help = State()
    fill_legal_assistance = State()
    fill_psycholog_support = State()
    fill_help_centers = State()
    fill_all_police_stations = State()
    fill_your_question_police = State()
    fill_your_question_medical = State()
    fill_all_medical_center = State()
    fill_change_sity = State()
    fill_change_country = State()
    fill_change_latitude = State()
    fill_change_longitude = State()
    fill_change_info = State()
    fill_change_psyinput = State()
    fill_change_legalreason = State()
    fill_change_policeinput = State()
    fill_change_medinput = State()
    fill_change_safety = State()
    fill_correct_psychological_support = State()
    fill_phone_list_return_main = State()
