from aiogram import F, Router, html
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from fluentogram import TranslatorRunner
from states.states import NatsTestSG

# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart())
async def process_start_command(message: Message, i18n: TranslatorRunner, state: FSMContext):
    username = html.quote(message.from_user.full_name)
    # Создаем объект инлайн-кнопки
    button = InlineKeyboardButton(
        text=i18n.button.button(),
        callback_data='button_pressed'
    )
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Отправляем сообщение пользователю
    await message.answer(
        text=i18n.hello.user(username=username),
        reply_markup=markup
    )
    # Устанавливаем состояние пользователя в состояние по умолчанию
    await state.set_state()


# Этот хэндлер срабатывает на команду /update
@user_router.message(Command(commands='update'))
async def process_update_command(message: Message, i18n: TranslatorRunner, state: FSMContext):
    # Отправляем пользователю сообщение с предложением прислать любой текст
    await message.answer(text=i18n.send.text())
    # Устанавливаем состояние ожидания ввода текста
    await state.set_state(NatsTestSG.enter_text)
    

# Этот хэндлер срабатывает на команду /read
@user_router.message(Command(commands='read'))
async def process_read_command(message: Message, state: FSMContext):
    # Получаем FSM data
    data = await state.get_data()
    # Отправляем в телеграм-клиент строковое представление FSM data
    await message.answer(text=str(data))


# Этот хэндлер срабатывает на любой текст в состоянии `NatsTestSG.enter_text`
@user_router.message(F.text, StateFilter(NatsTestSG.enter_text))
async def process_text_message(message: Message, i18n: TranslatorRunner, state: FSMContext):
    # Обновляем FSM data
    await state.update_data(text_data=message.text)
    # Отправляем пользователю сообщение о том, что текст успешно сохранен
    await message.answer(text=i18n.successfully.saved())
    # Возвращаем состояние в состояние по умолчанию
    await state.set_state()


# Этот хэндлер срабатывает на любое нетекстовое сообщение в состоянии `NatsTestSG.enter_text`
@user_router.message(StateFilter(NatsTestSG.enter_text))
async def process_any_message(message: Message, i18n: TranslatorRunner, state: FSMContext):
    # Отправляем пользователю сообщение о том, что ожидаем только текст
    await message.answer(text=i18n.text.only())


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
@user_router.callback_query(F.data == 'button_pressed')
async def process_button_click(callback: CallbackQuery, i18n: TranslatorRunner):
    await callback.answer(text=i18n.button.pressed())
