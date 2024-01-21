import asyncio
from datetime import datetime

from aiogram import types
from aiogram.types import BotCommand

import buttons as btn
from config import ADMIN_CHANNEL, ADMINS, CHAT_ID

from loader import bot, set_uname


from loguru import logger
import aioschedule

command = [
    BotCommand("start", "Перезапуск бота"),
    BotCommand("help", "Помощь по боту"),
    BotCommand("subscribe", "Проверить свою подписку"),
    BotCommand('help_adm', 'Помощь администратору')
]


async def on_shutdown(dp):
    for admin in ADMINS:
        await bot.send_message(admin, "Я закрылся!")


async def on_startup(dp):
    #asyncio.create_task(scheduler())  # Запускаем планировщик
    await bot.set_my_commands(command)


if __name__ == '__main__':
    from aiogram import executor

    from handlers import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
