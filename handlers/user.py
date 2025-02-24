from aiogram import Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from fluentogram import TranslatorRunner
from nats.js.client import JetStreamContext

from services.delay_service.publisher import delay_message_deletion


# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер будет срабатывать на команду /start
@user_router.message(CommandStart())
async def process_start_command(message: Message, i18n: TranslatorRunner):
    username = html.quote(message.from_user.full_name)
    await message.answer(text=i18n.hello.user(username=username))


# Этот хэндлер будет срабатывать на команду /del
@user_router.message(Command('del'))
async def send_and_del_message(
    message: Message,
    i18n: TranslatorRunner,
    js: JetStreamContext,
    delay_del_subject: str
) -> None:

    delay = 3
    msg: Message = await message.answer(text=i18n.will.delete(delay=delay))

    await delay_message_deletion(
        js=js,
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        subject=delay_del_subject,
        delay=delay
    )
