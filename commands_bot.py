from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/holiday", description="Узнать какой сегодня праздник"),
        BotCommand(command="/bus", description="Когда автобус"),
        BotCommand(command="/matches", description="Посмотреть проценты выигрыша на матчи")
    ]
    await bot.set_my_commands(commands)