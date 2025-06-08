from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
from keyboards.builders import keyboard


router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот дающий советы.\n"
                         "/help для вывода списка доступных команд",
                         reply_markup=keyboard)

    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("help"))
async def start_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - приветсвие\n"
        "/slip <id> - выдать совет по id(от 1 до 224)\n"
        "/randomslip - рандомный совет\n"
        "/favs - избранное\n"
        "/add_id <id> - добавить в избранное\n"
        "/del_id <id> - удалить из избранного\n"
        "/help- команды\n"
        "/support- поддержка"
    )
