from aiogram import F, Router
from aiogram.filters import (Command,
                             CommandStart,
                             StateFilter)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import (StatesGroup,
                               State,
                               default_state)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery,
                           Message)

from config_data.config import get_coord
from database.methods import (country_get,
                              town_get_police,
                              town_get_hospital,
                              town_get_help_center)
from keyboards.set_menu import (create_main_menu,
                                create_return_to_main_menu,
                                create_geo_lacation,
                                create_need_help,
                                create_choose_shar_or_not,
                                create_user_safe,
                                create_share_geo_bot,
                                create_data_confirmation,
                                create_not_location,
                                create_choosing_type_help,
                                create_points,
                                create_description_territory,
                                create_time_point_departure,
                                create_contact_emergency_services,
                                create_information_verification,
                                create_correct_information,
                                create_type_help,
                                create_phone_list,
                                create_need_police,
                                create_need_medical_help,
                                create_variables,
                                create_back_change,
                                create_after_share_geo_bot,
                                create_send_or_enter,
                                create_main_menu_not_geo,
                                create_all_centers)
from lexicon.lexicon_ru import (LEXICON,
                                LEXICON_DATA_CONFIRMATION)
from database.models import (user_dict,
                             data_variable)
from utils.utils import (translate_country,
                         translate_text)

router = Router()

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()




# Создаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_country = State()        # Состояние ожидания ввода страны при старте бота
    fill_town = State()         # Состояние ожидания ввода города при старте бота
    fill_need_help = State()  # Состояние ожидания выбора нужна помощь или нет
    fill_shar_geo = State()  # Состояние ожидания запроса доступа к гео
    fill_enter_geo = State()  # Состояние ожидания доступа к гео
    fill_enter_geo_main_menu = State()  # Состояние ожидания доступа к гео из главного меню
    fill_shar_geo_main_menu = State() # Состояние ожидания запроса к гео из главного меню
    fill_return_shar_geo_main_menu = State() # Состояние ожидания запроса к возврату из уточнения гео в главное меню
    fill_user_safe = State()  # Состояние ожидания запроса в безопасности ли пользователь
    fill_user_share_geo_bot = State() # Состояние ожидания подтверждения помощи поделиться геолокацией
    fill_return_shar_geo_clip = State() # Состояние ожидания геопозиции из меню СКРЕПКА
    fill_user_share_geo_bot_map = State() # Состояние ожидания включения геолокации
    fill_choosing_type_help = State() # Состояние ожидания выбора вида помощи пользователю
    fill_points_wifi_bluetooth = State() # Состояние ожидания ввода точек wifi и bluetooth
    fill_description_territory = State() # Состояние ожидания ввода описания территории
    fill_time_point_departure = State() # Состояние ожидания ввода описания отправных данных
    fill_contact_emergency_services = State() # Состояние ожидания связи с экстренными службами
    fill_security_confirmation = State() # Состояние ожидания подтверждения безопасности после определения гео
    fill_information_verification = State() # Состояние ожидания подтверждения введенной информации
    fill_correct_information = State() # Состояние ожидания корректировки информации
    fill_phone_list = State() # Состояние ожидания выбора звонка с телеграм
    fill_need_police = State() # Состояние ожидания выбора действия в меню полиции
    fill_need_medical_help = State() # Состояние ожидания выбора действия в меню мед помощи
    fill_legal_assistance = State() # Состояние ожидания ввода основания в меню юр помощи
    fill_psycholog_support = State() # Состояние ожидания ввода описания псих состояния
    fill_help_centers = State() # Состояние ожидания выбора действия в меню центров помощи
    fill_all_police_stations = State() # Состояние ожидания выбора действия в меню списка всех участков полиции
    fill_your_question_police = State() # Состояние ожидания ввода вопроса в меню полиции
    fill_your_question_medical = State() # Состояние ожидания ввода вопроса в меню мед помощи
    fill_all_medical_center = State() # Состояние ожидания выбора действия в меню списка всех мед центров
    fill_change_sity = State() # Состояние ожидания изменения города пользователя
    fill_change_country = State() # Состояние ожидания изменения страны пользователя
    fill_change_latitude = State() # Состояние ожидания изменения широты
    fill_change_longitude = State() # Состояние ожидания изменения долготы
    fill_change_info = State() # Состояние ожидания изменения информации о месте пребывания пользователя
    fill_change_psyinput = State() # Состояние ожидания изменения информации о состоянии пользователя
    fill_change_legalreason = State() # Состояние ожидания изменения информации о легальности пользователя
    fill_change_policeinput = State() # Состояние ожидания изменения вопроса полиции
    fill_change_medinput = State() # Состояние ожидания изменения вопроса медчасти
    fill_change_safety = State() # Состояние ожидания изменения вопроса безопасности пользователя
    fill_correct_psychological_support = State() # Состояние ожидания корректуры психологического состояния
    fill_phone_list_return_main = State() # Состояние просмотра sos телефонов или возврата в главное меню



# Этот хэндлер будет срабатывать на команду '/start' и запускать стартовое меню (шаг 2)
@router.message(CommandStart())
async def process_start_bot(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'],
                         reply_markup=create_main_menu())
    await state.clear()

# Этот хэндлер будет срабатывать на команду '/main_menu' и запускать начальное меню (шаг 2),
# главное меню (шаг 7), или меню безопасности (шаг 6)
@router.message(Command('main_menu'))
async def process_go_main_menu(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/start'],
                         reply_markup=create_main_menu())
    await state.clear()

# Этот хэндлер будет срабатывать на команду '/clean_history' и запускать начальное меню (шаг 2),
# главное меню (шаг 7), или меню безопасности (шаг 6)
@router.message(Command('clean_history'))
async def process_clean_history(message: Message, state: FSMContext):
    user_dict[message.from_user.id] = {}
    await message.answer(text=LEXICON['/start'],
                         reply_markup=create_main_menu())
    await state.clear()

# Этот хэндлер будет срабатывать на команду ГЛАВНОЕ МЕНЮ (шаг 0.1) и запускать начальное меню (шаг 2),
# главное меню (шаг 7), или меню безопасности (шаг 6)
@router.callback_query(F.data == 'return_main_menu')
async def process_go_main_menu(callback: CallbackQuery, state: FSMContext):
    try:
        if (user_dict[callback.message.chat.id]['country'] and
                user_dict[callback.message.chat.id]['sity'] and
                user_dict[callback.message.chat.id]['safety'].lower() == 'да'):
            await callback.message.answer(text=LEXICON['type_help'],
                                          reply_markup=create_type_help())
        elif (user_dict[callback.message.chat.id]['country'] and
              user_dict[callback.message.chat.id]['sity'] and
              user_dict[callback.message.chat.id]['safety'].lower() == 'нет'):
            await callback.message.answer(text=LEXICON['type_help'],
                                          reply_markup=create_choosing_type_help())
        else:
            await callback.message.answer(text=LEXICON['/start'],
                                          reply_markup=create_main_menu())
    except KeyError:
        await callback.message.answer(text=LEXICON['/start'],
                                      reply_markup=create_main_menu())
    await state.clear()

# Этот хэндлер будет срабатывать на команду '/change_data' и показывает пользователю его данные
@router.message(Command("change_data"))
async def process_change_data(message: Message):
    # Формирование сообщения из словаря
    try:
        await message.answer(text=LEXICON['change_data'],)
        for key, value in user_dict[message.from_user.id].items():
            await message.answer(text=f"{data_variable[key]}: {value}\n",)
        await message.answer(text=LEXICON['change'],
                             reply_markup=create_variables(message.from_user.id))
    except KeyError:
        await message.answer(text=f'{LEXICON["no_data"]}\n\n'
                                  f'{LEXICON["/start"]}',
                             reply_markup=create_main_menu())



# Этот хэндлер будет срабатывать нажатие кнопки НАЗАД (шаг 0.2) и показывает пользователю его данные
@router.callback_query(F.data == 'back_change',
                       StateFilter(default_state))
async def process_change_data_button(callback: CallbackQuery):
    # Формирование сообщения из словаря
    await callback.message.answer(text=LEXICON['change_data'],)
    for key, value in user_dict[callback.message.chat.id].items():
        await callback.message.answer(text=f"{data_variable[key]}: {value}\n",)
    await callback.message.answer(text=LEXICON['change'],
                                  reply_markup=create_variables(callback.message.chat.id))
    await callback.message.answer(text=LEXICON['no_data'],)


# Этот хэндлер будет срабатывать на нажатие кнопки смены города пребывания
@router.callback_query(F.data == 'sity')
async def process_change_sity(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_sity'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_sity)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_sity)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['sity'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()





# Этот хэндлер будет срабатывать на нажатие кнопки смены страны пребывания
@router.callback_query(F.data == 'country')
async def process_change_country(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_country'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_country)
    await callback.answer()

# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_country)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['country'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены широты
@router.callback_query(F.data == 'latitude')
async def process_change_latitude(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_latitude'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_latitude)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_latitude)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['latitude'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены долготы
@router.callback_query(F.data == 'longitude')
async def process_change_longitude(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_longitude'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_longitude)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_longitude)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['longitude'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены информации о месте пребывания пользователя
@router.callback_query(F.data == 'info')
async def process_change_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_info'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_info)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_info)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['info'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены информации о состоянии пользователя
@router.callback_query(F.data == 'psyinput')
async def process_change_psyinput(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_psyinput'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_psyinput)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_psyinput)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['psyinput'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены легальности
@router.callback_query(F.data == 'legalreason')
async def process_change_legalreason(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_legalreason'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_legalreason)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_legalreason)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['legalreason'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены вопроса полиции
@router.callback_query(F.data == 'policeinput')
async def process_change_policeinput(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_policeinput'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_policeinput)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_policeinput)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['policeinput'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие кнопки смены вопроса медпомощи
@router.callback_query(F.data == 'medinput')
async def process_change_medinput(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_medinput'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_medinput)
    await callback.answer()


# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_medinput)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['medinput'] = message.text
    await message.answer(text=LEXICON['change_data'], )
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()

# Этот хэндлер будет срабатывать на нажатие кнопки смены безопасности
@router.callback_query(F.data == 'safety')
async def process_change_safety(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['enter_new_value_safety'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_change_safety)
    await callback.answer()

# Этот хэндлер будет срабатывать на изменение данных пользователя
@router.message(FSMFillForm.fill_change_safety)
async def process_change_user_data(message: Message, state: FSMContext):
    user_dict[message.from_user.id]['safety'] = message.text
    await message.answer(text=LEXICON['change_data'],)
    for key, value in user_dict[message.from_user.id].items():
        await message.answer(text=f"{data_variable[key]}: {value}\n", )
    await message.answer(text=LEXICON['change'],
                         reply_markup=create_variables(message.from_user.id))
    await state.clear()





# Этот хэндлер будет срабатывать на команду '/hide_bot' и переводит пользователя на другой канал
@router.message(Command("hide_bot"))
async def go_to_channel(message: Message):
    await message.answer(f"Перейти на канал: https://t.me/Kulinariya_retsept")


# Этот хэндлер будет срабатывать на нажатие кнопки ввода страны и города (шаг 2)
# и переводит бота в состояние ожидания ввода страны (шаг 3.1)
@router.callback_query(F.data.in_({'country_town', 'turned_out', 'made_by'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_user_share_geo_bot_map,
                                   FSMFillForm.fill_contact_emergency_services))
async def process_enter_country(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['country'],
                                  reply_markup=create_return_to_main_menu())
    # Устанавливаем состояние ожидания ввода страны
    await state.set_state(FSMFillForm.fill_country)
    await callback.answer()


# Этот хэндлер будет срабатывать после ввода страны нахождения (шаг 3.1)
# и переводить бота в состояние ожидания ввода города (шаг 3.1)
@router.message(StateFilter(FSMFillForm.fill_country))
async def process_enter_town(message: Message, state: FSMContext):
    # Сохраняем страну в хранилище по ключу "country"
    await state.update_data(country=message.text)
    # Сохраняем код страны в хранилище по ключу "country_cod"
    await state.update_data(country_cod=message.from_user.language_code)
    await message.answer(text=LEXICON['town'],
                         reply_markup=create_return_to_main_menu())
    # Устанавливаем состояние ожидания ввода города
    await state.set_state(FSMFillForm.fill_town)

# Этот хэндлер будет срабатывать после ввода города нахождения (шаг 3.1), сохранять данные,
# запрашивать подтверждение введенных данных (шаг 4.1) и выводить из машины состояний
@router.message(StateFilter(FSMFillForm.fill_town))
async def process_enter_town(message: Message, state: FSMContext):
    # Сохраняем город в хранилище по ключу "sity"
    await state.update_data(sity=message.text)
    # Добавляем в базу данных анкету пользователя
    user_dict[message.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await message.answer(text=f'Подтверди свою геопозицию\n'
                              f'Ваша страна: {user_dict[message.from_user.id]['country']}\n'
                              f'Ваш город: {user_dict[message.from_user.id]['sity']}',
                         reply_markup=create_data_confirmation())


# Этот хэндлер будет возвращать в начальное меню (шаг 2) при нажатии кнопки НАЗАД (шаг 3.1, шаг 2.1)
@router.callback_query(F.data == 'return_to_main_menu',
                       StateFilter(default_state,
                                   FSMFillForm.fill_country,
                                   FSMFillForm.fill_town))
async def process_return_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['/start'],
                                  reply_markup=create_main_menu())
    await state.clear()
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки ДАТЬ ДОСТУП К МЕСТОПОЛОЖЕНИЮ (шаг 2)
# и запрашивать доступ к геолокации через обычную кнопку (шаг 3.2)
@router.callback_query(F.data.in_({'share_location', 'turned_out'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_user_share_geo_bot_map))
async def process_callback_share_location(callback: CallbackQuery):
    # Отправляем сообщение с просьбой поделиться геолокацией
    await callback.message.answer(text=LEXICON['request_give_geo'],
                                  reply_markup=create_return_to_main_menu())
    await callback.message.answer(text=LEXICON['give_access_location'],
                                  reply_markup=create_geo_lacation())

    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки ОТПРАВИТЬ СВОЮ ГЕОЛОКАЦИЮ (шаг 3.2),
# сохранять данные местоположения и ожидать подтверждения данных
@router.message(F.location,
                StateFilter(default_state))
async def handle_location(message: Message, state: FSMContext):
    await state.update_data(latitude=message.location.latitude)
    await state.update_data(longitude=message.location.longitude)
    user_dict[message.from_user.id] = await state.get_data()
    try:
        user_id = message.from_user.id
        res = get_coord(geocode=f'{user_dict[user_id]['longitude']},{user_dict[user_id]['latitude']}')
        result = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["description"]
        user_dict[user_id]['sity'] = result.split()[-2]
        user_dict[user_id]['country'] = result.split()[-1]
        user_dict[user_id]['country_cod'] = message.from_user.language_code
        await message.answer(text=f'Ваша страна {user_dict[user_id]['country']}\n'
                                  f'Ваш город {user_dict[user_id]['sity']}\n'
                                  f'Ваши координаты:\nШирота: {user_dict[user_id]['latitude']}\n'
                                  f'Долгота: {user_dict[user_id]['longitude']}',
                             reply_markup=create_data_confirmation(),)
    except Exception:
        await message.answer(text=LEXICON['not_location'],
                             reply_markup=create_main_menu(),)


# Этот хэндлер будет срабатывать на нажатие кнопки Я НЕ ЗНАЮ ГДЕ Я (шаг 2) и НАЗАД (шаг 3.4)
# и переводит бота в состояние выбора нужна помощь или нет (шаг 3.3)
@router.callback_query(F.data.in_({'dont_know_where_i', 'return_to_need_help'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_shar_geo))
async def process_enter_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['need_help'],
                                  reply_markup=create_need_help(),)
    # Устанавливаем состояние ожидания выбора нужна помощь или нет
    await state.set_state(FSMFillForm.fill_need_help)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки НЕ НАДО (шаг 3.3) и НАЗАД (шаг 3.2)
# и переводит бота в состояние запроса геоположения (шаг 3.4)
@router.callback_query(F.data.in_({'not_help_me', 'return_to_not_share_geo'}),
                       StateFilter(FSMFillForm.fill_need_help))
async def process_not_share_geo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['not_share_geo'],
                                  reply_markup=create_choose_shar_or_not(),)
    # Устанавливаем состояние ожидания выбора нужна помощь или нет
    await state.set_state(FSMFillForm.fill_shar_geo)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопку Я НЕ БУДУ ДАВАТЬ СВОЕ ГЕО (ШАГ 2)
# из главного меню и ПРОПУСТИТЬ ШАГ С ГЕО (ШАГ 3.3.3) и переводит бота в состояние запроса геоположения (ШАГ 3.2)
@router.callback_query(F.data.in_({'not_location_access', 'return_to_share_geo', 'skip_geo_step'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_return_shar_geo_main_menu,
                                   FSMFillForm.fill_contact_emergency_services))
async def process_too_not_share_geo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['too_not_share_geo'],
                                  reply_markup=create_choose_shar_or_not(),)
    # Устанавливаем состояние ожидания выбора нужна помощь или нет
    await state.set_state(FSMFillForm.fill_shar_geo_main_menu)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки "ПОДЕЛИТЬСЯ ГЕО" (шаг 3.4 от шага 3.3)
# и переводит бота в состояние запроса гео (шаг 3.2)
@router.callback_query(F.data == 'share_location',
                       FSMFillForm.fill_shar_geo)
async def process_callback_share_location_too(callback: CallbackQuery, state: FSMContext):
    # Отправляем сообщение с просьбой поделиться геолокацией
    await callback.message.answer(text='request_give_geo',
                                  reply_markup=create_return_to_main_menu())
    await callback.message.answer(text=LEXICON['give_access_location'],
                                  reply_markup=create_geo_lacation())
    await state.set_state(FSMFillForm.fill_enter_geo)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки "ПОДЕЛИТЬСЯ ГЕО" (шаг 3.4 шаг 2)
# по пути от главного меню и переводит бота в состояние запроса гео (шаг 3.2)
@router.callback_query(F.data == 'share_location',
                       FSMFillForm.fill_shar_geo_main_menu)
async def process_callback_share_location_too(callback: CallbackQuery, state: FSMContext):
    # Отправляем сообщение с просьбой поделиться геолокацией
    await callback.message.answer(text=LEXICON['give_access_location'],
                                  reply_markup=create_geo_lacation())
    await state.set_state(FSMFillForm.fill_enter_geo_main_menu)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки ОТПРАВИТЬ СВОЮ ГЕОЛОКАЦИЮ (шаг 3.2),
# сохранять данные местоположения и ожидать подтверждения данных
@router.message(F.location,
                StateFilter(FSMFillForm.fill_enter_geo))
async def handle_location_too(message: Message, state: FSMContext):
    await state.update_data(latitude=message.location.latitude)
    await state.update_data(longitude=message.location.longitude)
    user_dict[message.from_user.id] = await state.get_data()
    try:
        user_id = message.from_user.id
        res = get_coord(geocode=f'{user_dict[user_id]['longitude']},{user_dict[user_id]['latitude']}')
        result = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["description"]
        user_dict[user_id]['sity'] = result.split()[-2]
        user_dict[user_id]['country'] = result.split()[-1]
        user_dict[user_id]['country_cod'] = message.from_user.language_code
        await message.answer(text=f'Ваша страна {user_dict[user_id]['country']}\n'
                                  f'Ваш город {user_dict[user_id]['sity']}\n'
                                  f'Ваши координаты:\nШирота: {user_dict[user_id]['latitude']}\n'
                                  f'Долгота: {user_dict[user_id]['longitude']}',
                             reply_markup=create_data_confirmation(),)
        await state.set_state(FSMFillForm.fill_need_help)
    except Exception:
        await message.answer(text=LEXICON['not_location'],
                             reply_markup=create_main_menu(),)
        await state.clear()

# Этот хэндлер будет срабатывать на нажатие кнопки ОТПРАВИТЬ СВОЮ ГЕОЛОКАЦИЮ,
# сохранять данные местоположения и ожидать подтверждения данных (шаг 4.1)
@router.message(F.location,
                StateFilter(FSMFillForm.fill_enter_geo_main_menu))
async def handle_location_too(message: Message, state: FSMContext):
    await state.update_data(latitude=message.location.latitude)
    await state.update_data(longitude=message.location.longitude)
    user_dict[message.from_user.id] = await state.get_data()
    try:
        user_id = message.from_user.id
        res = get_coord(geocode=f'{user_dict[user_id]['longitude']},{user_dict[user_id]['latitude']}')
        result = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["description"]
        user_dict[user_id]['sity'] = result.split()[-2]
        user_dict[user_id]['country'] = result.split()[-1]
        user_dict[user_id]['country_cod'] = message.from_user.language_code
        await message.answer(text=f'Ваша страна {user_dict[user_id]['country']}\n'
                                  f'Ваш город {user_dict[user_id]['sity']}\n'
                                  f'Ваши координаты:\nШирота: {user_dict[user_id]['latitude']}\n'
                                  f'Долгота: {user_dict[user_id]['longitude']}',
                             reply_markup=create_data_confirmation(),)
        await state.set_state(FSMFillForm.fill_return_shar_geo_main_menu)
    except Exception:
        await message.answer(text=LEXICON['not_location'],
                             reply_markup=create_main_menu(),)
        await state.clear()



# Этот хэндлер будет возвращать в меню ДЛЯ ТОЧНОЙ ПОМОЩИ (шаг 3.4 от 2)
# по пути сразу в главное меню при нажатии кнопки НАЗАД (шаг 3.2)
@router.callback_query(F.data == 'return_to_need_help',
                       StateFilter(FSMFillForm.fill_shar_geo_main_menu))
async def process_return_to_enter_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['/start'],
                                  reply_markup=create_main_menu())
    await state.clear()
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопки ПОМОГИ (шаг 3.3)
# и переводит в состояние ожидания выбора находится ли пользователь в безопасности или нет (шаг 3.3.1)
@router.callback_query(F.data == 'help_me',
                       StateFilter(FSMFillForm.fill_need_help))
async def process_help_me(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['help_me'],
                                  reply_markup=create_user_safe())
    await state.set_state(FSMFillForm.fill_user_safe)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопки ДА (шаг 3.3.1) в безопасности, инструктирует пользователя
# как поделиться геолокацией через бот и переводит в состояние ожидания действия (шаг 3.3.2.1)
@router.callback_query(F.data == 'user_to_safe',
                       StateFilter(FSMFillForm.fill_user_safe))
async def process_share_geo_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['share_geo_bot'],
                                  reply_markup=create_after_share_geo_bot(),)
    await state.set_state(FSMFillForm.fill_user_share_geo_bot)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки ГЕОПОЗИЦИЯ в меню СКРЕПКА (шаг 3.3.2.1),
# сохранять координаты местоположения и спрашивать о результатах запроса геолокации (шаг 4.1)
@router.message(F.location,
                StateFilter(FSMFillForm.fill_user_share_geo_bot))
async def handle_location_too(message: Message, state: FSMContext):
    await state.update_data(latitude=message.location.latitude)
    await state.update_data(longitude=message.location.longitude)
    user_dict[message.from_user.id] = await state.get_data()
    try:
        user_id = message.from_user.id
        res = get_coord(geocode=f'{user_dict[user_id]['longitude']},{user_dict[user_id]['latitude']}')
        result = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["description"]
        user_dict[user_id]['sity'] = result.split()[-2]
        user_dict[user_id]['country'] = result.split()[-1]
        user_dict[user_id]['country_cod'] = message.from_user.language_code
        await message.answer(text=f'Ваша страна {user_dict[user_id]['country']}\n'
                                  f'Ваш город {user_dict[user_id]['sity']}\n'
                                  f'Ваши координаты:\nШирота: {user_dict[user_id]['latitude']}\n'
                                  f'Долгота: {user_dict[user_id]['longitude']}',
                             reply_markup=create_share_geo_bot(),)
        await state.set_state(FSMFillForm.fill_return_shar_geo_clip)
    except Exception:
        await message.answer(text=LEXICON['not_location'],
                             reply_markup=create_main_menu(),)
        await state.clear()




# Этот хэндлер будет срабатывать на нажатие кнопок НЕ ПОЛУЧИЛОСЬ и ДРУГОЙ СПОСОБ (шаг 3.3.2.1)
# вместо проверки геопозиции из меню скрепка, инструктирует пользователя как включить геолокацию
# и переводит в состояние ожидания действия (шаг 3.3.2.4)
@router.callback_query(F.data.in_({'another_way', 'not_turned_out'}),
                       StateFilter(FSMFillForm.fill_return_shar_geo_clip,
                                   FSMFillForm.fill_user_share_geo_bot))
async def process_share_geo_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['another_way'],
                                  reply_markup=create_share_geo_bot())
    await state.set_state(FSMFillForm.fill_user_share_geo_bot_map)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопок НЕ ПОЛУЧИЛОСЬ и ДРУГОЙ СПОСОБ (шаг 3.3.2.4)
# вместо включения геопозиции, просит пользователя определить точки WI-FI и Bluetooth,
# и переводит в состояние ожидания ввода описания (шаг 3.3.2.6)
@router.callback_query(F.data.in_({'another_way', 'not_turned_out'}),
                       StateFilter(FSMFillForm.fill_user_share_geo_bot_map))
async def process_points_wifi_bluetooth(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['points_wifi_bluetooth'],
                                  reply_markup=create_points())
    await state.set_state(FSMFillForm.fill_points_wifi_bluetooth)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопок НЕТ ТОЧЕК и ДРУГОЙ СПОСОБ (шаг 3.3.2.6)
# при поиске точек WI-FI и Bluetooth, просит пользователя описать что находится рядом,
# и переводит в состояние ожидания ввода описания (шаг 3.3.2.7)
@router.callback_query(F.data.in_({'not_points', 'another_points'}),
                       StateFilter(FSMFillForm.fill_points_wifi_bluetooth))
async def process_description_territory(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['description_territory'],
                                  reply_markup=create_description_territory())
    await state.set_state(FSMFillForm.fill_description_territory)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопок НЕ ВИЖУ и ДРУГОЙ СПОСОБ (шаг 3.3.2.7)
# при описании местонахождения, просит пользователя описать точку отправления и время в пути,
# и переводит в состояние ожидания ввода описания (шаг 3.3.2.8)
@router.callback_query(F.data.in_({'not_see', 'another_see'}),
                       StateFilter(FSMFillForm.fill_description_territory))
async def process_time_point_departure(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['time_point_departure'],
                                  reply_markup=create_time_point_departure())
    await state.set_state(FSMFillForm.fill_time_point_departure)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопок НЕ ЗНАЮ и ДРУГОЙ СПОСОБ (шаг 3.3.2.8)
# при описании точки отправления, НЕТ (шаг 3.3.1), просит пользователя связаться с экстренными службами,
# и переводит в состояние ожидания связи со службами (шаг 3.3.3)
@router.callback_query(F.data.in_({'not_know', 'another_know', 'another_stap', 'user_not_safe'}),
                       StateFilter(FSMFillForm.fill_time_point_departure,
                                   FSMFillForm.fill_correct_information,
                                   FSMFillForm.fill_information_verification,
                                   FSMFillForm.fill_user_safe))
async def process_contact_emergency_services(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['contact_emergency_services'],
                                  reply_markup=create_contact_emergency_services())
    await state.set_state(FSMFillForm.fill_contact_emergency_services)
    await callback.answer()



# Этот хэндлер будет срабатывать после ввода описания точек WIFI (шаг 3.3.2.6), местонахождения (шаг 3.3.2.7)
# или точки отправления (шаг 3.3.2.8), просит пользователя проверить введенную информацию
# и переводит бота в состояние ожидания подтверждения введенной информации (шаг 3.3.2.9)
@router.message(StateFilter(FSMFillForm.fill_points_wifi_bluetooth,
                            FSMFillForm.fill_description_territory,
                            FSMFillForm.fill_time_point_departure,
                            FSMFillForm.fill_correct_information))
async def process_information_verification(message: Message, state: FSMContext):
    # Сохраняем информацию в хранилище по ключу "info"
    if message.from_user.id not in user_dict:
        user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['info'] = message.text
    await message.answer(text=f'Проверь верно ли я все записала:\n'
                              f'{user_dict[message.from_user.id]['info']}',
                         reply_markup=create_information_verification())
    # Устанавливаем состояние ожидания подтверждения информации
    await state.set_state(FSMFillForm.fill_information_verification)



# Этот хэндлер будет срабатывать на нажатие кнопок ИСПРАВИТЬ (шаг 3.3.2.9),
# просит пользователя заново ввести информацию,
# и переводит в состояние ожидания корректировки информации (шаг 3.3.2.9.1)
@router.callback_query(F.data == 'correct_information',
                       StateFilter(FSMFillForm.fill_information_verification))
async def process_correct_information(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['correct_information'],
                                  reply_markup=create_correct_information())
    await state.set_state(FSMFillForm.fill_correct_information)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки НЕТ (шаг 4.1) и ПОПРОБОВАТЬ ЕЩЕ РАЗ (шаг 4.2),
# когда данные местоположения не соответствуют, сбрасывает машину состояний и переводит бота в стартовое меню (шаг 2.1)
@router.callback_query(F.data.in_({'not_confirm', 'try_again_location'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_need_help,
                                   FSMFillForm.fill_return_shar_geo_main_menu,
                                   FSMFillForm.fill_return_shar_geo_clip))
async def process_repeat_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['repeat_main_menu'],
                                  reply_markup=create_main_menu_not_geo())
    await state.clear()
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки ДА (шаг 3.3.2.9), ОТПРАВИТЬ (шаг 3.3.2.9.1, шаг 6.5, шаг 8.4, шаг 8.5) и отправлять данные в ИИ



# Этот хэндлер будет срабатывать, когда местоположение не определено, предлагает (шаг 4.2)
# заново определить местоположение, обратиться в SOS или пропустить определение местоположение
@router.callback_query(F.data.in_({'not_share_location', 'another_services'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_shar_geo,
                                   FSMFillForm.fill_shar_geo_main_menu,
                                   FSMFillForm.fill_contact_emergency_services))
async def process_contact_sos_or_try_again(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['not_share_location'],
                                  reply_markup=create_not_location())
    await state.clear()
    await callback.answer()



# Этот хэндлер будет срабатывать на нажатие кнопка ДА (шаг 4.1) при подтверждении гео
# и ПРОПУСТИТЬ ПОИСК МЕСТОПОЛОЖЕНИЯ (шаг 4.2), и переводить бота в меню безопасности (шаг 5)
@router.callback_query(F.data.in_({'confirm', 'skip_location_search', 'turned_out'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_need_help,
                                   FSMFillForm.fill_return_shar_geo_main_menu,
                                   FSMFillForm.fill_return_shar_geo_clip))
async def process_security_confirmation(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"{LEXICON['skip_location_search']}",
                                  reply_markup=create_data_confirmation())
    await state.set_state(FSMFillForm.fill_security_confirmation)
    await callback.answer()



# Этот хэндлер будет срабатывать на нажатие кнопок ДА (шаг 5) при подтверждении безопасности пользователя,
# Я В БЕЗОПАСНОСТИ при выборе вида помощи (шаг 6), В ГЛАВНОЕ МЕНЮ (шаг 8.1, 8.1.1, 8.2, 8.2.1, 8.3)
# меню полиции, мед помощи и центров помощи, НАЗАД (шаг 8.3) сохраняет в переменную safety
# и переводить бота в главное меню (шаг 7)
@router.callback_query(F.data.in_({'confirm', 'i_safe', 'main_menu', 'back_change'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_security_confirmation,
                                   FSMFillForm.fill_choosing_type_help,
                                   FSMFillForm.fill_help_centers,
                                   FSMFillForm.fill_need_police,
                                   FSMFillForm.fill_need_medical_help,
                                   FSMFillForm.fill_all_police_stations,
                                   FSMFillForm.fill_all_medical_center,
                                   FSMFillForm.fill_psycholog_support,
                                   FSMFillForm.fill_legal_assistance))
async def process_type_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['type_help'],
                                  reply_markup=create_type_help())
    if callback.message.chat.id not in user_dict:
        user_dict[callback.message.chat.id] = {}
    user_dict[callback.message.chat.id]['safety'] = LEXICON_DATA_CONFIRMATION['confirm']
    await state.clear()
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопки НЕТ (шаг 5) при запросе в безопасности ли пользователь,
# /
# сохраняет в переменную safety и переводить бота в состояние ожидания выбора вида помощи (шаг 6)
@router.callback_query(F.data.in_({'not_confirm', 'not_call', 'back_change'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_security_confirmation,
                                   FSMFillForm.fill_phone_list,
                                   FSMFillForm.fill_choosing_type_help))
async def process_choosing_type_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"{LEXICON['user_not_safe']}",
                                  reply_markup=create_choosing_type_help())
    if callback.message.chat.id not in user_dict:
        user_dict[callback.message.chat.id] = {}
    user_dict[callback.message.chat.id]['safety'] = LEXICON_DATA_CONFIRMATION['not_confirm']
    await state.set_state(FSMFillForm.fill_choosing_type_help)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопки НАЗАД (шаг 6.2) и возвращать в главное меню (шаг 7)
@router.callback_query(F.data.in_({'not_call'}),
                       StateFilter(FSMFillForm.fill_phone_list_return_main))
async def process_choosing_type_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['type_help'],
                                  reply_markup=create_type_help(),)
    await callback.message.answer(f'{await state.get_state()}')
    await state.clear()
    await callback.message.answer(f'{await state.get_state()}')
    await callback.answer()




# Этот хэндлер будет срабатывать на нажатие кнопок ВЫЗВАТЬ ЭКСТРЕННУЮ ПОМОЩЬ (шаг 6) при выборе вида помощи,
# ОБРАТИТЬСЯ В SOS (шаг 4.2) если нет местоположения,
# предоставлять список телефонов, и переводить бота в состояние ожидания выбора действия (шаг 6.2)
@router.callback_query(F.data.in_({'emergency_assistance', 'contact_SOS'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_choosing_type_help))
async def process_phone_list(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    try:
        country_translate = translate_country(chat_id, user_dict[chat_id]['country']).strip(' .')
        country_translate = country_translate.split()
        country_translate = ' '.join(country_translate[1:])
        country_info = await country_get(country_translate)
        if country_info:
            await callback.message.answer(text=f'{LEXICON['phone_list']}\n'
                                               f'Страна: {user_dict[chat_id]['country']}\n'
                                               f'Общий номер экстренных служб: {country_info['shared_number']}\n'
                                               f'Полиция: {country_info['police']}\n'
                                               f'Скорая помощь: {country_info['ambulance']}\n'
                                               f'Пожарная служба: {country_info['fire_department']}\n'
                                               f'Регион: {country_info['region']}\n'
                                               f'Телефонный код: {country_info['phone_code']}\n'
                                               f'Дополнительная информация: {country_info['information']}\n',
                                          reply_markup=create_phone_list())
        else:
            await callback.message.answer(text=f'{LEXICON['phone_list_1']}\n',
                                          reply_markup=create_phone_list())
    except Exception:
        await callback.message.answer(text=LEXICON['not_location'],
                                      reply_markup=create_main_menu(), )
        await state.clear()
    await state.set_state(FSMFillForm.fill_phone_list)
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие кнопки SOS ТЕЛЕФОНЫ и SOS ПОМОЩ (шаг 7) из меню безопасности,
# предоставлять список телефонов, и переводить бота в состояние ожидания выбора действия (шаг 6.2)
@router.callback_query(F.data.in_({'sos_phones', 'sos_help'}),
                       # StateFilter(default_state,
                       #             FSMFillForm.fill_choosing_type_help)
                       )
async def process_phone_list(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    try:
        country_translate = translate_country(chat_id, user_dict[chat_id]['country']).strip(' .')
        country_translate = country_translate.split()
        country_translate = ' '.join(country_translate[1:])
        country_info = await country_get(country_translate)
        if country_info:
            await callback.message.answer(text=f'{LEXICON['phone_list']}\n'
                                               f'Страна: {user_dict[chat_id]['country']}\n'
                                               f'Общий номер экстренных служб: {country_info['shared_number']}\n'
                                               f'Полиция: {country_info['police']}\n'
                                               f'Скорая помощь: {country_info['ambulance']}\n'
                                               f'Пожарная служба: {country_info['fire_department']}\n'
                                               f'Регион: {country_info['region']}\n'
                                               f'Телефонный код: {country_info['phone_code']}\n'
                                               f'Дополнительная информация: {country_info['information']}\n',
                                          reply_markup=create_phone_list())
        else:
            await callback.message.answer(text=f'{LEXICON['phone_list_1']}\n',
                                          reply_markup=create_phone_list())
    except Exception:
        await callback.message.answer(text=LEXICON['not_location'],
                                      reply_markup=create_main_menu(), )
        await state.clear()
    await state.set_state(FSMFillForm.fill_phone_list_return_main)
    await callback.answer()



# Этот хэндлер будет срабатывать на нажатие кнопки ПСИХОЛОГИЧЕСКАЯ ПОДДЕРЖКА (шаг 6) при выборе вида помощи,
# просит пользователя описать свое состояние (шаг 6.5), и выводить бота из меню состояний
@router.callback_query(F.data == 'psychological_support',
                       StateFilter(FSMFillForm.fill_choosing_type_help))
async def process_psychological_support(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f'{LEXICON["psychological_support"]}',
                                  reply_markup=create_back_change(),)

    await callback.answer()


# Этот хэндлер будет срабатывать после ввода описания психологического состояния (шаг 6.5)
# и выводить бота из меню состояний
# !!!!!!!!!!!!!!!!!!!!!Здесь нужно будет переносить данные в ИИ (шаг 3.3.2.10)
@router.message(StateFilter(FSMFillForm.fill_choosing_type_help))
async def process_message_psychological_support(message: Message, state: FSMContext):
    # Сохраняем информацию в хранилище по ключу "psyinput"
    if message.from_user.id not in user_dict:
        user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['psyinput'] = message.text
    await message.answer(text=f'Проверь верно ли я все записала:\n'
                              f'{user_dict[message.from_user.id]['psyinput']}',
                         reply_markup=create_send_or_enter(),)
    # Выводим из машины состояний
    await state.set_state(FSMFillForm.fill_correct_psychological_support)

# Этот хэндлер будет срабатывать на нажатие кнопок ИСПРАВИТЬ (шаг 6.5), просит пользователя заново ввести информацию,
# и переводит в состояние ожидания корректировки информации
@router.callback_query(F.data == 'correct_information',
                       StateFilter(FSMFillForm.fill_correct_psychological_support))
async def process_correct_information(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['correct_information'],)
    await state.set_state(FSMFillForm.fill_choosing_type_help)
    await callback.answer()




# Этот хэндлер будет срабатывать на нажатие кнопки НУЖНА ПОЛИЦИЯ (шаг 7) главного меню
# и переводить бота в меню полиции (шаг 8.1)
@router.callback_query(F.data.in_({'need_police', 'back_change'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_your_question_police))
async def process_need_police(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['need_police'],
                                  reply_markup=create_need_police())
    await state.set_state(FSMFillForm.fill_need_police)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки НУЖНА МЕДИЦИНСКАЯ ПОМОЩЬ (шаг 7)
# главного меню и переводить бота в меню мед помощи (шаг 8.2)
@router.callback_query(F.data.in_({'need_medical_help', 'back_change'}),
                       StateFilter(default_state,
                                   FSMFillForm.fill_your_question_medical))
async def process_need_medical_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['need_medical_help'],
                                  reply_markup=create_need_medical_help())
    await state.set_state(FSMFillForm.fill_need_medical_help)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки ЮРИДИЧЕСКАЯ ПОМОЩЬ (шаг 7) главного меню
# и переводить бота в состояние ожидания ввода текста юридической помощи (шаг 8.4)
@router.callback_query(F.data == 'legal_assistance',
                       StateFilter(default_state))
async def process_legal_assistance(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['legal_assistance'],
                                  reply_markup=create_back_change(),)
    await state.set_state(FSMFillForm.fill_legal_assistance)
    await callback.answer()

# Этот хэндлер будет срабатывать после ввода основания в меню юр помощи (шаг 8.4),
# сохранять в переменную legalreason и просить пользователя проверить введенную информацию
# !!!!!!!!!!!!!!!!!!!!!Здесь нужно будет переносить данные в ИИ (шаг 3.3.2.10)
@router.message(StateFilter(FSMFillForm.fill_legal_assistance))
async def process_enter_legal_assistance(message: Message, state: FSMContext):
    # Сохраняем информацию в хранилище по ключу "legalreason"
    if message.from_user.id not in user_dict:
        user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['legalreason'] = message.text
    await message.answer(text=f'Проверь верно ли я все записала:\n'
                              f'{user_dict[message.from_user.id]['legalreason']}',
                         reply_markup=create_send_or_enter())
    # Устанавливаем состояние подтверждения информации
    await state.set_state(FSMFillForm.fill_change_legalreason)


# Этот хэндлер будет срабатывать на нажатие кнопок ИСПРАВИТЬ в меню юридической помощи,
# просит пользователя заново ввести информацию, и переводит в состояние ожидания корректировки информации
@router.callback_query(F.data == 'correct_information',
                       StateFilter(FSMFillForm.fill_change_legalreason))
async def process_correct_information(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['correct_information'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_legal_assistance)
    await callback.answer()




# Этот хэндлер будет срабатывать на нажатие кнопки ПСИХОЛОГИЧЕСКАЯ ПОДДЕРЖКА (шаг 7) главного меню
# и переводить бота в состояние ожидания ввода текста психологической поддержки (шаг 8.5)
@router.callback_query(F.data == 'psycholog_support',
                       StateFilter(default_state))
async def process_psycholog_support(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['psycholog_support'],
                                  reply_markup=create_back_change(),)
    await state.set_state(FSMFillForm.fill_psycholog_support)
    await callback.answer()

# Этот хэндлер будет срабатывать после ввода псих состояние в меню псих поддержки (шаг 8.5),
# сохранять в переменную psyinput и просить пользователя проверить введенную информацию
# !!!!!!!!!!!!!!!!!!!!!Здесь нужно будет переносить данные в ИИ (шаг 3.3.2.10)
@router.message(StateFilter(FSMFillForm.fill_psycholog_support))
async def process_enter_psycholog_support(message: Message, state: FSMContext):
    # Сохраняем информацию в хранилище по ключу "psyinput"
    if message.from_user.id not in user_dict:
        user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['psyinput'] = message.text

    await message.answer(text=f'Проверь верно ли я все записала:\n'
                              f'{user_dict[message.from_user.id]['psyinput']}',
                         reply_markup=create_send_or_enter())
    # Устанавливаем состояние подтверждения информации
    await state.set_state(FSMFillForm.fill_change_psyinput)

# Этот хэндлер будет срабатывать на нажатие кнопок ИСПРАВИТЬ в меню псих поддержки,
# просит пользователя заново ввести информацию, и переводит в состояние ожидания корректировки информации
@router.callback_query(F.data == 'correct_information',
                       StateFilter(FSMFillForm.fill_change_psyinput))
async def process_correct_information(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['correct_information'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_psycholog_support)
    await callback.answer()



# Этот хэндлер будет срабатывать на нажатие кнопки ЦЕНТРЫ ПОМОЩИ (шаг 7) главного меню
# и переводить бота в меню центров помощи (шаг 8.3)
@router.callback_query(F.data == 'help_centers',
                       StateFilter(default_state))
async def process_help_centers(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    if user_dict:
        text_translate = translate_text(chat_id, user_dict[chat_id]['sity']).strip(' .')
        text_translate = text_translate.split()
        text_translate = ' '.join(text_translate[1:])
        country_translate = translate_country(chat_id, user_dict[chat_id]['country']).strip(' .')
        country_translate = country_translate.split()
        country_translate = ' '.join(country_translate[1:])
        print(text_translate, '!', country_translate)
        town_info_help_center = await town_get_help_center(town=text_translate, country=country_translate)
        if town_info_help_center:
            await callback.message.answer(text=f'{LEXICON['help_centers']}\n')
            for town in town_info_help_center:
                await callback.message.answer(text=f'Город: {town['city']}\n'
                                                   f'Адрес: {town['address']}\n'
                                                   f'Организация: {town['organization']}\n'
                                                   f'Описание: {town['description']}\n'
                                                   f'Телефон: {town['phone']}\n'
                                                   f'SOS телефон: {town['sos_phone']}\n'
                                                   f'Почта: {town['email']}\n'
                                                   f'Сайт: {town['website']}\n',)
        await callback.message.answer(text=f'-----',
                                      reply_markup=await create_all_centers(chat_id,
                                                                            callback.message.chat.full_name,
                                                                            LEXICON['show_all_hospitals']))
        await state.set_state(FSMFillForm.fill_help_centers)
        await callback.answer()
    else:
        await callback.message.answer(text=LEXICON['repeat_main_menu'],
                                      reply_markup=create_main_menu())
        await state.clear()
        await callback.answer()



# Этот хэндлер будет срабатывать на нажатие кнопки НАЙТИ УЧАСТОК ПОЛИЦИИ (шаг 8.1)
# меню полиции и, если есть ГЕО, то показывать список участков полиции (шаг 8.1.1),
# а если нет, то возвращать в стартовое меню (шаг 2.1)
@router.callback_query(F.data == 'find_police_station',
                       StateFilter(FSMFillForm.fill_need_police))
async def process_all_police_stations(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    try:
        text_translate = translate_text(chat_id, user_dict[chat_id]['sity']).strip(' .')
        text_translate = text_translate.split()
        text_translate = ' '.join(text_translate[1:])
        country_translate = translate_country(chat_id, user_dict[chat_id]['country']).strip(' .')
        country_translate = country_translate.split()
        country_translate = ' '.join(country_translate[1:])
        town_info_police = await town_get_police(text_translate, country_translate)
        if town_info_police:
            await callback.message.answer(text=f'{LEXICON['find_police_station']}\n',)
            for town in town_info_police:
                await callback.message.answer(text=f'Город: {town['city']}\n'
                                                   f'Адрес: {town['address']}\n'
                                                   f'Телефон: {town['phone']}\n'
                                                   f'Название: {town['name']}\n\n',)
            await callback.message.answer(text=f'-----',
                                          reply_markup=await create_all_centers(chat_id,
                                                                                callback.message.chat.full_name,
                                                                                LEXICON['show_all_police_city']))
        await state.set_state(FSMFillForm.fill_all_police_stations)
        await callback.answer()
    except Exception as e:
        print(e)
        await callback.message.answer(text=LEXICON['repeat_main_menu'],
                                      reply_markup=create_main_menu())
        await state.clear()
        await callback.answer()




# Этот хэндлер будет срабатывать на нажатие кнопки СВОЙ ВОПРОС (шаг 8.1) меню полиции
# и переводить бота в ожидание ввода вопроса (шаг 8.2.2)
@router.callback_query(F.data == 'your_question',
                       StateFilter(FSMFillForm.fill_need_police))
async def process_your_question_police(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['your_question'],
                                  reply_markup=create_back_change(),)
    await state.set_state(FSMFillForm.fill_your_question_police)
    await callback.answer()


# Этот хэндлер будет срабатывать после ввода своего вопроса из меню полиции (шаг 8.2.2),
# сохранять его в переменную policeinput и просит пользователя сверить введенную информацию
# !!!!! Передача вопроса ИИ
@router.message(StateFilter(FSMFillForm.fill_your_question_police))
async def process_saving_police_issue(message: Message, state: FSMContext):
    # Сохраняем вопрос в хранилище по ключу "policeinput"
    if message.from_user.id not in user_dict:
        user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['policeinput'] = message.text

    await message.answer(text=f'Проверь верно ли я все записала\n'
                              f'{user_dict[message.from_user.id]['policeinput']}',
                         reply_markup=create_send_or_enter(),)
    # Устанавливаем состояние подтверждения информации
    await state.set_state(FSMFillForm.fill_change_policeinput)


# Этот хэндлер будет срабатывать на нажатие кнопок ИСПРАВИТЬ в свой вопрос из меню полиции,
# просит пользователя заново ввести информацию, и переводит в состояние ожидания корректировки информации
@router.callback_query(F.data == 'correct_information',
                       StateFilter(FSMFillForm.fill_change_policeinput))
async def process_correct_information(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['correct_information'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_your_question_police)
    await callback.answer()





# Этот хэндлер будет срабатывать на нажатие кнопки НАЙТИ МЕД ЦЕНТР (шаг 8.2) меню мед центров
# и, если есть ГЕО, то показывать список мед центров (шаг 8.2.1), а если нет, то возвращать в стартовое меню (шаг 2.1)
@router.callback_query(F.data == 'find_medical_center',
                       StateFilter(FSMFillForm.fill_need_medical_help))
async def process_all_medical_center(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    try:
        text_translate = translate_text(chat_id, user_dict[chat_id]['sity']).strip(' .')
        text_translate = text_translate.split()
        text_translate = ' '.join(text_translate[1:])
        country_translate = translate_country(chat_id, user_dict[chat_id]['country']).strip(' .')
        country_translate = country_translate.split()
        country_translate = ' '.join(country_translate[1:])
        town_info_hospitals = await town_get_hospital(text_translate, country_translate)
        if town_info_hospitals:
            await callback.message.answer(text=f'{LEXICON['find_medical_center']}\n',)
            for town in town_info_hospitals:
                    await callback.message.answer(text=f'Город: {town['city']}\n'
                                                       f'Адрес: {town['address']}\n'
                                                       f'Телефон: {town['phone']}\n'
                                                       f'Название: {town['name']}\n'
                                                       f'Описание: {town['description']}\n'
                                                       f'Почта: {town['email']}\n'
                                                       f'Сайт: {town['website']}\n',)
            await callback.message.answer(text=f'-----',
                                          reply_markup=await create_all_centers(chat_id,
                                                                                callback.message.chat.full_name,
                                                                                LEXICON['show_all_hospitals']))
        await state.set_state(FSMFillForm.fill_all_medical_center)
        await callback.answer()
    except Exception:
        await callback.message.answer(text=LEXICON['repeat_main_menu'],
                                      reply_markup=create_main_menu())
        await state.clear()
        await callback.answer()



# Этот хэндлер будет срабатывать на нажатие кнопки СВОЙ ВОПРОС (шаг 8.2) меню мед центров
# и переводить бота в ожидание ввода вопроса (шаг 8.2.2)
@router.callback_query(F.data == 'your_question',
                       StateFilter(FSMFillForm.fill_need_medical_help))
async def process_your_medical_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['your_question'],
                                  reply_markup=create_back_change(),)
    await state.set_state(FSMFillForm.fill_your_question_medical)
    await callback.answer()


# Этот хэндлер будет срабатывать после ввода своего вопроса из меню мед центров (шаг 8.2),
# сохранять его в переменную medinput и просить проверить введенную информацию
# !!!!! Передача вопроса ИИ
@router.message(StateFilter(FSMFillForm.fill_your_question_medical))
async def process_saving_medical_issue(message: Message, state: FSMContext):
    # Сохраняем вопрос в хранилище по ключу "medinput"
    if message.from_user.id not in user_dict:
        user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['medinput'] = message.text

    await message.answer(text=f'Проверь верно ли я все записала\n'
                              f'{user_dict[message.from_user.id]['medinput']}',
                         reply_markup=create_send_or_enter(),)
    # Устанавливаем состояние подтверждения информации
    await state.set_state(FSMFillForm.fill_change_medinput)


# Этот хэндлер будет срабатывать на нажатие кнопок ИСПРАВИТЬ в свой вопрос из меню мед центров,
# просит пользователя заново ввести информацию, и переводит в состояние ожидания корректировки информации
@router.callback_query(F.data == 'correct_information',
                       StateFilter(FSMFillForm.fill_change_medinput))
async def process_correct_information(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['correct_information'],
                                  reply_markup=create_back_change())
    await state.set_state(FSMFillForm.fill_your_question_medical)
    await callback.answer()