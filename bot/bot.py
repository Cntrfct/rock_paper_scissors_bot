import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import other_handlers, user_handlers
from handlers.user_handlers import set_main_menu

# Создаем логгер
logger = logging.getLogger(__name__)


# Функция конфигурации и запуска бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # Выводим в консоль инфо о запуске бота
    logger.info('Starting bot...')

    # Загружаем конфиг в config
    config: Config = load_config()

    # Создаём бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Регистрируем роутеры  и меню в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    dp.startup.register(set_main_menu)

    # Пропускаем апдейты и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
