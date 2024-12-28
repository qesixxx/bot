from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import StateFilter
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from base_for_expiry import Equipment, equipment_database
from aiogram.types.web_app_info import WebAppInfo
import json



# Инициализация бота и диспетчера
API_TOKEN = '7601003095:AAHPSElCSqC2nWjFD3YKm-s_pD0xJ3V4Hkc'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Хранилище для состояний
dp = Dispatcher(storage=storage)

# Состояния
class UserStates(StatesGroup):
    WAITING_FOR_FIO = State()
    WAITING_FOR_PASSWORD = State()
    LOGGED_IN = State()


user_data = {}


# Функции для работы с файлом пользователей
def load_users_from_file():
    if not os.path.exists('users.json'):
        # Если файл не существует, создаем его с пустым словарем
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump({}, file)
        return {}

    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Если файл содержит некорректный JSON, возвращаем пустой словарь
        return {}

def save_users_to_file(users):
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


# Загружаем данные при старте бота
users = load_users_from_file()


@dp.message(Command("start"))
async def main(message: types.Message, state: FSMContext):
    user_id = str(message.chat.id)
    if user_id in users:
        # Если пользователь уже зарегистрирован, пропускаем ввод ФИО
        await state.set_state(UserStates.LOGGED_IN)
        await message.reply(f'С возвращением, {users[user_id]["first_name"]} {users[user_id]["last_name"]}!')
        await send_main_menu(message)
    else:
        # Если пользователь новый, запрашиваем ФИО
        await state.set_state(UserStates.WAITING_FOR_FIO)
        await message.reply(f'Здравствуйте, {message.from_user.first_name}! Вы используете бот ПСТ. Для регистрации и прохождения далее введите ФИО.')

@dp.message(StateFilter(UserStates.WAITING_FOR_FIO))
async def handle_fio(message: types.Message, state: FSMContext):
    parts = message.text.split()
    if len(parts) >= 3:
        if all(part.isalpha() for part in parts):  # Проверяем, что все части ФИО состоят из букв
            first_name = parts[1]
            last_name = parts[0]
            patronymic = parts[2]

            # Сохраняем данные пользователя в user_data
            user_id = str(message.chat.id)  # Используем строковый ключ
            user_data[user_id] = {
                'first_name': first_name,
                'last_name': last_name,
                'patronymic': patronymic
            }

            # Логирование
            print(f"Данные пользователя {user_id} сохранены в user_data: {user_data[user_id]}")

            await state.set_state(UserStates.WAITING_FOR_PASSWORD)
            await message.reply(f'Отлично, {first_name} {last_name}, теперь введите код доступа для взаимодействия с предприятием.')
        else:
            await message.reply('Пожалуйста, введите ФИО, используя только буквы.')
    else:
        await message.reply('Пожалуйста, введите полное ФИО (фамилия, имя, отчество) через пробел.')

# Обработчик для ввода пароля
@dp.message(StateFilter(UserStates.WAITING_FOR_PASSWORD))
async def handle_password(message: types.Message, state: FSMContext):
    user_id = str(message.chat.id)  # Используем строковый ключ

    # Проверяем, есть ли данные пользователя в user_data
    if user_id not in user_data:
        await message.reply('Ошибка: данные пользователя не найдены. Пожалуйста, начните с команды /start.')
        return

    if message.text == 'password123':
        await message.reply('Обрабатываю запрос . . . ')
        await message.reply('Вы успешно вошли в систему.')
        await state.set_state(UserStates.LOGGED_IN)

        # Сохраняем данные пользователя в файл
        users[user_id] = user_data[user_id]  # Сохраняем данные из user_data в users
        save_users_to_file(users)  # Сохраняем в файл

        # Логирование
        print(f"Данные пользователя {user_id} сохранены в users.json: {users[user_id]}")

        # Отправляем главное меню
        await send_main_menu(message)
    else:
        await message.reply('Обрабатываю запрос . . . ')
        await message.reply('Неверный код доступа.')

async def send_main_menu(message: types.Message):
    # Путь к вашей картинке
    image_path = os.path.join('img', 'menu_photo.jpg')

    # Проверка, существует ли файл
    if not os.path.exists(image_path):
        await message.answer("Картинка не найдена!")
        return

    # Создание клавиатуры с кнопками (используем InlineKeyboardBuilder)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Перейти на официальный сайт ПСТ', url='https://этпп.рф/'))
    builder.row(types.InlineKeyboardButton(text='Срок эксплуатации по ЭПБ', callback_data='expiry'))
    builder.row(types.InlineKeyboardButton(text='! ! ! Произошла авария ! ! !', callback_data='accident'))
    builder.row(types.InlineKeyboardButton(
        text='Просмотреть паспорт оборудования',
        callback_data='passport'  # Указываем callback_data для обработки нажатия
    ))

    markup = builder.as_markup()

    # Отправка фотографии и кнопок
    photo = FSInputFile(image_path)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption='Выберите действие:',
        reply_markup=markup
    )


@dp.callback_query(lambda call: call.data == 'passport')
async def handle_passport_button(call: types.CallbackQuery):
    # Создаем клавиатуру с кнопкой, открывающей веб-приложение
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='Открыть список оборудования', web_app=WebAppInfo(url='https://www.deepseek.com/'))]
        ],
        resize_keyboard=True  # Опционально: автоматическое изменение размера клавиатуры
    )

    # Отправляем сообщение с клавиатурой
    await call.message.answer('Откройте список оборудования по кнопке ниже или введите идентификатор', reply_markup=markup)

    # Подтверждаем обработку callback-запроса
    await call.answer()

# Обработчик для callback_data='accident'
@dp.callback_query(lambda call: call.data == 'accident')
async def handle_accident(call: types.CallbackQuery):
    await call.answer()  # Ответ на callback_query
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='ОПО "Наименование № 1"', callback_data='first_opo')],
            [InlineKeyboardButton(text='ОПО "Наименование № 2"', callback_data='second_opo')],
            [InlineKeyboardButton(text='В главное меню', callback_data='main_menu_return')]
        ]
    )
    await call.message.answer('Выберите опасный производственный объект, (далее - ОПО) на котором произошла авария', reply_markup=markup)

@dp.callback_query(lambda call: call.data == 'main_menu_return')
async def handle_main_menu_return(call: types.CallbackQuery):
    # Создаем объект message из call
    message = call.message
    # Отправляем главное меню
    await send_main_menu(message)


def get_greeting(patronymic):
    if patronymic.endswith(('вна', 'чна')):  # Женские отчества
        return 'Уважаемая'
    elif patronymic.endswith(('вич', 'ьич')):  # Мужские отчества
        return 'Уважаемый'
    else:
        return 'Уважаемый/Уважаемая'  # Если отчество не удалось определить


@dp.callback_query(lambda call: call.data == 'first_opo')
async def handle_first_opo(call: types.CallbackQuery):
    await call.answer()  # Ответ на callback_query

    # Получаем данные пользователя
    user_id = str(call.message.chat.id)
    user_info = users.get(user_id, {})  # Используем данные из файла

    # Определяем пол на основе отчества
    patronymic = user_info.get('patronymic', '')
    greeting = get_greeting(patronymic)

    # Формируем сообщение
    message_text = (
        f'{greeting}, {user_info.get("first_name", "")} {user_info.get("last_name", "")}!\n\n'
        'Произошла аварийная ситуация.\n'
        'В течение 24 часов необходимо передать информацию об аварии, следующим лицам/службам:\n'
        '- Директор производства (тел. +7 000 000 00 00);\n'
        '- Ростехнадзор (тел. +7 000 000 00 00);\n'
        '- Администрация города (тел. +7 000 000 00 00);\n'
        '- Скорая помощь (при наличии пострадавших) (тел. +7 000 000 00 00);\n'
        '- Пожарная охрана (тел. +7 000 000 00 00);\n'
        '- Аварийно-спасательное формирование (тел. +7 000 000 00 00);\n'
        '- Государственная инспекция труда (тел. +7 000 000 00 00).'
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Назад', callback_data='accident')],
            [InlineKeyboardButton(text='В главное меню', callback_data='main_menu_return')]
        ]
    )

    # Отправляем сообщение с кнопкой "Назад"
    await call.message.answer(message_text, reply_markup=markup)




# Обработчик для callback_data='back_warning'
@dp.callback_query(lambda call: call.data == 'back_warning')
async def handle_back_warning(call: types.CallbackQuery):
    await handle_accident(call)



# Обработчик для callback_data='expiry'
@dp.callback_query(lambda call: call.data == 'expiry')
async def handle_expiry_button(call: types.CallbackQuery):
    expired_equipment = []
    expiring_soon_equipment = []
    active_equipment = []

    for equipment in equipment_database:
        if equipment.is_expired():
            expired_equipment.append(equipment)
        elif equipment.is_expiring_soon():
            expiring_soon_equipment.append(equipment)
        else:
            active_equipment.append(equipment)

    message = ""

    if expired_equipment:
        message += "Оборудование с истекшим сроком эксплуатации:\n"
        for equipment in expired_equipment:
            message += str(equipment) + "\n"
        message += "\n"

    if expiring_soon_equipment:
        message += "Оборудование с истекающим сроком эксплуатации:\n"
        for equipment in expiring_soon_equipment:
            message += str(equipment) + "\n"
        message += "\n"

    if active_equipment:
        message += "Действующее оборудование:\n"
        for equipment in active_equipment:
            message += str(equipment) + "\n"

    await bot.send_message(call.message.chat.id, message)

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True)