from aiogram import types
from aiogram import BaseMiddleware
from collections import defaultdict
from aiogram import types
import time
import asyncio


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit_interval=5, max_messages_per_interval=3, ban_time=60):
        """
        Инициализация middleware для антиспама.
        
        :param limit_interval: интервал времени в секундах для проверки лимита
        :param max_messages_per_interval: максимальное количество сообщений за интервал
        :param ban_time: время бана в секундах при превышении лимита
        """
        self.limit_interval = limit_interval
        self.max_messages = max_messages_per_interval
        self.ban_time = ban_time
        self.user_message_times = defaultdict(list)
        self.banned_users = {}
        
        super().__init__()

    async def __call__(self, handler, message: types.Message, data: dict):
        user_id = message.from_user.id
        current_time = time.time()

        # Проверка на бан
        if user_id in self.banned_users:
            if current_time < self.banned_users[user_id]:
                # Пользователь все еще забанен
                await message.answer("Вы отправляете сообщения слишком часто. Пожалуйста, подождите.")
                return
            else:
                # Бан закончился
                del self.banned_users[user_id]
                self.user_message_times[user_id] = []

        # Очистка старых сообщений
        self.user_message_times[user_id] = [
            t for t in self.user_message_times[user_id] 
            if current_time - t < self.limit_interval
        ]

        # Добавление времени текущего сообщения
        self.user_message_times[user_id].append(current_time)

        # Проверка на превышение лимита
        if len(self.user_message_times[user_id]) > self.max_messages:
            # Бан пользователя
            self.banned_users[user_id] = current_time + self.ban_time
            await message.answer(
                f"Вы отправляете слишком много сообщений. Пожалуйста, подождите {self.ban_time} секунд."
            )
            return
        return await handler(message, data)
