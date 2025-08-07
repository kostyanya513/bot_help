"""
Словари с текстовыми константами для бота на русском языке.

Здесь определены тексты сообщений и команд для различных состояний и меню.
"""
LEXICON: dict[str, str] = {
    '/start': '<b>Привет, солнце, это Горгона!</b>\n\n'
              'Расскажи мне, что у тебя случилось и мы сможем найти'
              ' выход вместе!\n\n'
              'Для начала мне надо знать находишься ли <b>ты сейчас'
              ' в безопасности?</b>\n'
              'Укажи, пожалуйста, в какой стране и городе ты находишься'
              ' сейчас?\n\n'
              '<b>SOS телефон:</b> 0800100007 с 10:00 до 20:00\n\n'
              '<b>Полиция:</b>192 (tel:192)\n\n'
              'Иностранная сим-карта:\n+381 21 192 Нови Сад\n+381 11 192'
              ' Белград\n\n'
              'Местная сим-карта:\n0 21 192 Нови Сад\n0 11 192 Белград',
    'another_way': 'Включи геолокацию в настройках телефона\n'
                   'Зайди в любое приложение с картами или через ссылки'
                   ' в браузере:\n'
                   'google maps\n'
                   'Apple maps',
    'all_places': 'Все участки в городе мед, полиция и тд',
    'country': 'Введите вашу страну',
    'data_development': 'Данные по этой стране и городу находятся в разработке!',
    'description_territory': 'Хорошо, давай попробуем по описанию\n'
                             'Посмотри вокруг. Видишь ли ты таблички'
                             ' с названиями улиц, номера зданий, магазины,'
                             ' остановки транспорта?',
    'help_me': 'Для начала мне надо знать, ты сейчас находишься в'
               ' безопасности?',
    'contact_emergency_services': 'Определение через звонок в экстренные'
                                  ' службы\n'
                                  'Номер экстренной службы (112 или 911).\n'
                                  'Опиши ситуацию и запроси помощь'
                                  ' в определении местоположения.'
                                  ' Операторы могут использовать данные'
                                  ' сотовой сети для примерного'
                                  ' определения местоположения.',
    'correct_information': 'Пожалуйста скопируй сообщение и'
                           ' внеси изменения',
    'change_data': 'Вот данные о тебе:',
    'change': 'Если надо что-то поменять выбери переменную и'
              ' отправь измененный параметр',
    'enter_new_value_sity': 'Введите Город',
    'enter_new_value_country': 'Введите Страну',
    'enter_new_value_latitude': 'Введите Широту',
    'enter_new_value_longitude': 'Введите Долготы',
    'enter_new_value_info': 'Введите информацию о месте своего'
                            ' пребывания',
    'enter_new_value_psyinput': 'Введите Ваше состояние',
    'enter_new_value_legalreason': 'Введите Легальность',
    'enter_new_value_policeinput': 'Введите вопрос полиции',
    'enter_new_value_medinput': 'Введите вопрос медпомощи',
    'enter_new_value_safety': 'Вы находитесь в безопасности?',
    'find_police_station': 'Полиция\n'
                           'Вот список полицейских участков на'
                           ' основе геопозиции:',
    'find_medical_center': 'Мед помощь\n'
                           'Вот список мед учреждений на основе'
                           ' геопозиции:',
    'give_access_location': 'Разреши доступ к геоположению',
    'how_call': 'SOS телефоны\n'
                'Это как объяснение',
    'help_centers': 'Центры помощи\n'
                    'На основе вашей геопозиции вот центры помощи'
                    ' для вас:',
    'legal_assistance': 'Скажите, на каком основании вы находитесь'
                        ' в этой стране и городе?',
    'manipulative_techniques': 'Манипулятивные техники для'
                               ' обезвреживания насильника',
    'need_help': 'Для точной помощи, мне необходимо знать твое'
                 ' местоположение, давай я помогу тебе его определить?',
    'not_share_geo': 'Для точной помощи, мне необходимо знать твое'
                     ' местоположение, ты уверена что не хочешь'
                     ' делиться гео',
    'not_share_location': 'Нет местоположения\n'
                          'К сожалению нам не получилось узнать твое'
                          ' местоположение, я настоятельно рекомендую'
                          ' обратиться в службу спасения, особенно если'
                          ' есть угроза здоровью',
    'need_police': 'Полиция\n'
                   'Вы можете задать свой вопрос и я отвечу на него'
                   ' или же предоставить данные к вашему местоположению,'
                   ' чтобы я смогла найти ближайшие к вам участки полиции',
    'need_medical_help': 'Мед помощь\n'
                         'Вы можете задать свой вопрос и я отвечу на'
                         ' него или же я могу найти ближайший работающий'
                         ' центр мед помощи',
    'no_data': 'Вы не сохраняли никакие данные!',
    'no_data_available': 'нет данных',
    'not_location': 'Не удалось найти ваше местоположение',
    'points_wifi_bluetooth': 'Хорошо, давай попробуем по описанию\n'
                             'Определите ближайшие точки Wi-Fi или'
                             ' Bluetooth (могут быть видны в настройках).'
                             ' Их можно использовать для локального'
                             ' определения местоположения.',
    'phone_list': 'SOS телефоны:\n',
    'psycholog_support': 'Психологическая поддержка\n'
                         'Опишите свое состояние и какая помощь вам'
                         ' требуется',
    'psychological_support': 'Психологическая поддержка\n'
                             'Опишите свое состояние и какая помощь'
                             ' вам требуется',
    'phone_list_1': 'SOS телефоны:\n'
                    'гео не указан:позвоните по общему номеру службы'
                    ' спасения 911 или 112\n'
                    'Вы хотите позвонить через меня?',
    'repeat_main_menu': 'Укажите свое местоположение',
    'request_give_geo': 'Вы можете вернуться на шаг',
    'skip_location_search': 'Ты сейчас находишься в безопасности?',
    'self_defense_techniques': 'Техники самообороны',
    'show_all_hospitals': 'Покажи все больницы в городе',
    'show_all_police_city': 'Покажи все участки в городе',
    'show_all_centers': 'Покажи все центры',
    'share_geo_bot': 'Давай попробуем самое легкое:\n'
                     'Telegram позволяет пользователям отправить свою'
                     ' текущую геолокацию.\n'
                     'Инструкция для пользователя:\n'
                     'Нажмите на кнопку «скрепка» (иконка вложений) .\n'
                     'Выберите «Геопозиция».\n'
                     'Отправьте свою текущую локацию или включите «живую'
                     ' геолокацию», если нужно отслеживать перемещение.',
    'town': 'Спасибо!\n\nА теперь введите ваш город',
    'too_not_share_geo': 'Для точной помощи, мне необходимо знать твое'
                         ' местоположение, ты уверена что не хочешь делиться'
                         ' гео',
    'time_point_departure': 'Хорошо, давай попробуем по описанию\n'
                            'Сколько времени ты уже в пути?\n'
                            'Помнишь ли ты отправную точку?\n'
                            'Это может помочь приблизительно вычислить твоё'
                            ' местоположение.',
    'type_help': 'Укажи какая помощь тебе сейчас требуется',
    'tips_safe_place': 'Советы по уходу в безопасное место',
    'user_not_safe': 'Укажи какая помощь тебе сейчас требуется',
    'your_question': 'Задайте свой вопрос и я отвечу на него используя мое'
                     ' обучение и базы знаний',
}

LEXICON_COMMANDS: dict[str, str] = {
    '/main_menu': 'главное меню',
    '/clean_history': 'очищает историю',
    '/hide_bot': 'переносит в тг канал @kulinariya_retsept и очищает историю'
                 ' у user',
    '/change_data': 'изменить данные - выводит данные со всех переменных'
                    ' заполненных',
}

LEXICON_MAIN_MENU: dict[str, str] = {
    'country_town': 'Указать страну и город',
    'share_location': 'Дать доступ к местоположению',
    'dont_know_where_i': 'Я не знаю где я',
    'not_location_access': 'Я не буду давать своё гео',
}

LEXICON_MAIN_MENU_NOT_GEO: dict[str, str] = {
    'country_town': 'Указать страну и город',
    'share_location': 'Дать доступ к местоположению',
    'dont_know_where_i': 'Я не знаю где я',
    'not_location_access': 'Я не буду давать своё гео',
    'return_to_main_menu': 'Назад',
}

LEXICON_RETURN_TO_MAIN_MENU: dict[str, str] = {
    'return_to_main_menu': 'Назад',
}

LEXICON_NEED_HELP: dict[str, str] = {
    'help_me': 'Помоги',
    'not_help_me': 'Не надо',
    'return_to_main_menu': 'Назад',
}

LEXICON_CHOOSE_SHAR_OR_NOT: dict[str, str] = {
    'share_location': 'Поделиться гео',
    'not_share_location': 'Я не буду давать свое гео',
    'return_to_need_help': 'Назад',
}

LEXICON_RETURN_TO_NOT_SHARE_GEO: dict[str, str] = {
    'return_to_not_share_geo': 'Назад',
}

LEXICON_RETURN_TO_SHARE_GEO: dict[str, str] = {
    'return_to_share_geo': 'Назад',
}

LEXICON_USER_SAFE: dict[str, str] = {
    'user_to_safe': 'Да',
    'user_not_safe': 'Нет',
}

LEXICON_AFTER_METHOD_DETERMINING_GEO: dict[str, str] = {
    'not_turned_out': 'Не получилось',
    'another_way': 'Другой способ',
}

LEXICON_METHOD_DETERMINING_GEO: dict[str, str] = {
    'turned_out': 'Получилось',
    'not_turned_out': 'Не получилось',
    'another_way': 'Другой способ',
}

LEXICON_DATA_CONFIRMATION: dict[str, str] = {
    'confirm': 'Да',
    'not_confirm': 'Нет',
}

LEXICON_NOT_LOCATION: dict[str, str] = {
    'contact_SOS': 'Обратиться в sos',
    'skip_location_search': 'Пропустить поиск местоположения',
    'try_again_location': 'Попробовать ещё раз',
}

LEXICON_POINTS: dict[str, str] = {
    'not_points': 'Нет точек',
    'another_points': 'Другой способ',
}

LEXICON_DESCRIPTION_TERRITORY: dict[str, str] = {
    'not_see': 'Не вижу',
    'another_see': 'Другой способ',
}

LEXICON_CREATE_TIME_POINT_DEPARTURE: dict[str, str] = {
    'not_know': 'Не знаю',
    'another_know': 'Другой способ',
}

LEXICON_CONTACT_EMERGENCY_SERVICES: dict[str, str] = {
    'made_by': 'Сделаю!',
    'another_services': 'Другой способ',
    'skip_geo_step': 'Пропусти шаг с гео',
}

LEXICON_INFORMATION_VERIFICATION: dict[str, str] = {
    'right_information': 'Да',
    'correct_information': 'Исправить',
    'another_stap': 'Другой способ',
}

LEXICON_CORRECT_INFORMATION: dict[str, str] = {
    'another_stap': 'Другой способ',
}

LEXICON_TYPE_HELP: dict[str, str] = {
    'sos_phones': 'SOS телефоны',
    'need_police': 'Нужна полиция',
    'need_medical_help': 'Нужна медицинская помощь',
    'legal_assistance': 'Юридическая помощь',
    'psycholog_support': 'Психологическая поддержка',
    'help_centers': 'Центры помощи',
    'sos_help': 'SOS помощь!',
}

LEXICON_NEED_POLICE: dict[str, str] = {
    'find_police_station': 'Найти участок полиции',
    'your_question': 'Свой вопрос',
    'main_menu': 'В главное меню',
}

LEXICON_NEED_MEDICAL_HELP: dict[str, str] = {
    'find_medical_center': 'Найти мед центр',
    'your_question': 'Свой вопрос',
    'main_menu': 'В главное меню',
}

LEXICON_BACK_CHANGE: dict[str, str] = {
    'back_change': 'Назад',
}

LEXICON_SEND_OR_ENTER: dict[str, str] = {
    'to_send': 'Отправить',
    'correct_information': 'Исправить',
}
