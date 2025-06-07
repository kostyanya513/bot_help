from database.models import user_dict, user_tokens
from telegraph import Telegraph



from mymemopy.translator import MyMemoryTranslate


# Инициализация переводчика (анонимный пользователь)
translator = MyMemoryTranslate()

# Функция для перевода страны на английский язык
def translate_country(user_id, text):
    source_lang = user_dict[user_id]['country_cod']
    target_lang = 'en'
    country_lang = translator.translate(text=f'Country',
                                        source_lang='en',
                                        target_lang=source_lang)
    try:
        translation = translator.translate(text=f'{country_lang} {text}',
                                           source_lang=source_lang,
                                           target_lang=target_lang)
        return translation
    except Exception as e:
        return f"Ошибка перевода: {e}"

# Функция для перевода текста на язык пользователя
def translate_text(user_id, text):
    source_lang = user_dict[user_id]['country_cod']
    target_lang = 'en'
    town_lang = translator.translate(text=f'Town',
                                     source_lang=target_lang,
                                     target_lang=source_lang)
    target_lang = 'ru'
    print(text)
    print(town_lang)
    try:
        if target_lang == source_lang:
            return f'{town_lang} {text}'
        else:
            translation = translator.translate(text=f'{town_lang} {text}',
                                               source_lang=source_lang,
                                               target_lang='sr')
            return translation
    except Exception as e:
        return f"Ошибка перевода: {e}"

# Функция для получения или создания токена telegraph для пользователя
async def get_or_create_telegraph_token(user_id: int) -> str:
    """
    Получаем или создаём access_token для пользователя.
    В реальном приложении сохраняйте токен в БД.
    """
    if user_id in user_tokens:
        return user_tokens[user_id]

    telegraph = Telegraph()
    response = telegraph.create_account(short_name=f"user_{user_id}")
    access_token = response['access_token']
    user_tokens[user_id] = access_token
    return access_token


# Создаем ссылку на статью Telegraph
async def create_telegraph_article(access_token: str, title: str, author: str, content: list) -> str:
    telegraph = Telegraph(access_token=access_token)
    response = telegraph.create_page(title=title,
                                     author_name=author,
                                     content=content)
    return response['url']