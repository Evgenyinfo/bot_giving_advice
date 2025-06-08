from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from services.api_client import Client
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from random import randint
router = Router()

mal_client = Client()


# Использование: /slip <id>
@router.message(Command("slip"))
async def cmd_slip(message: Message):
    parts = message.text.split(maxsplit=1)

    slip_id = parts[1].strip()
    await get_slip(slip_id, message)


# Использование: /randomslip
@router.message(Command("randomslip"))
async def cmd_randomslip(message: Message):
    slip_id = randint(1, 224)
    await get_slip(slip_id, message)
    

async def get_slip(slip_id, message: Message):   
    try:
        response = await mal_client.get_slip(slip_id)
        response = response['slip']
        return await message.reply(f"Совет {response['id']}:\n {response['advice']}")
    except:
        return await message.reply(f"Произошла ошибка.")
    
    
