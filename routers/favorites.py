from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from services.favorites_storage import FavoritesStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.slip import mal_client, get_slip

router = Router()

# инициализируем хранилище (файл рядом с bot.py: storage/favorites.json)
storage = FavoritesStorage("storage/favorites.json")

# ---- Добавить в избранное ----
# Использование: /add_id <id>
@router.message(Command("add_id"))
async def cmd_add_fav(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 1:
        return await message.reply("Чтобы добавить совет напишите: /add_id 1")

    fav = parts[1].strip()
    # опционально можно проверить существование через mal_client.anime_exists
    await storage.add(message.from_user.id, fav)
    await message.reply(f"Совет {fav} добавлен в избранное.")

# ---- Список избранного ----
@router.message(Command("favs"))
async def cmd_list_fav(message: Message):
    favs = await storage.list(message.from_user.id)
    if not favs:
        return await message.reply("Пока нет избранного 🙁")
    text = "Ваше избранное:\n" + "\n".join(f"- {a}" for a in favs)
    # кнопки для выбора каждого:
    kb = InlineKeyboardBuilder()
    for fav in favs:
        kb.button(text=f"Совет {fav}", callback_data=f"send_slip_{fav}")
    kb.adjust(1)
    await message.reply(text, reply_markup=kb.as_markup())

# Выбрать по кнопке
@router.callback_query(lambda c: c.data.startswith("send_slip_"))
async def cmd_send_slip(query: CallbackQuery):
    fav = query.data.split("_", 2)[2]
    await query.answer(f"Совет {fav}", show_alert=False)
    await get_slip(fav, query.message)

# ---- Удалить из избранного командой ----
@router.message(Command("del_id"))
async def cmd_remove_fav(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Нужно id совета: /del_id 1")
    fav = parts[1].strip()
    await storage.remove(message.from_user.id, city)
    await message.reply(f"❌ Совет {fav} удален.")



