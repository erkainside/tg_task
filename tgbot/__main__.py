import asyncio
import logging
import betterlogging as bl
import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import handlers
from data import config
from database.sqlite import async_main
from utils.logger import log_to_channel
from handlers import setup
from handlers.exceptions import CustomErrorHandler


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")

def setup(dp: Dispatcher):
    # Регистрация обработчика ошибок
    dp.errors.middleware(CustomErrorHandler())


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.setup())


def setup_middlewares(dp: Dispatcher) -> None:
    pass


async def setup_aiogram(dp: Dispatcher, bot: Bot) -> None:
    setup_handlers(dp)
    setup_middlewares(dp)


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await setup_aiogram(dispatcher, bot)


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.session.close()
    await dispatcher.storage.close()


async def main():
    try:
        await async_main()
    except Exception as e:
        logging.error(f"Ошибеа при инициализации базы данных: {e}")
        return
    setup_logging()
    session = AiohttpSession(
        json_loads=orjson.loads,
    )

    bot = Bot(
        token=config.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    storage = MemoryStorage()

    dp = Dispatcher(
        storage=storage,
    )

    await setup_aiogram(dp, bot)
    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
