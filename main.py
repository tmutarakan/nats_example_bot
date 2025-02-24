import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fluentogram import TranslatorHub

from config_data.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
from middlewares.i18n import TranslatorRunnerMiddleware
from utils.i18n import create_translator_hub
from utils.nats_connect import connect_to_nats
from utils.start_consumers import start_delayed_consumer

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
            '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Подключаемся к NATS и получаем ссылки на клиент и JetStream-контекст
    nc, js = await connect_to_nats(servers=config.nats.servers)

    # Создаем объект типа TranslatorHub
    translator_hub: TranslatorHub = create_translator_hub()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Регистрируем миддлварь для i18n
    dp.update.middleware(TranslatorRunnerMiddleware())

    # Запускаем polling и консьюмер отложенного удаления сообщений
    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,
                delay_del_subject=config.delayed_consumer.subject,
                _translator_hub=translator_hub
            ),
            start_delayed_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=config.delayed_consumer.subject,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name
            )
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info('Connection to NATS closed')


asyncio.run(main())
