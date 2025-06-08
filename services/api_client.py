import time
import aiohttp
from aiohttp import ClientError, ClientTimeout
from random import randint
import json

class Client:
    def __init__(self, cache_ttl: int = 300000, timeout: int = 10):
        self.base_url = "https://api.adviceslip.com/advice"
        self.timeout = timeout  # Таймаут запроса в секундах

        self.cache: dict[str, tuple[float, dict]] = {}  # slip_id -> (timestamp, data)
        self.cache_ttl = cache_ttl  # Время жизни кэша в секундах

    async def get_slip(self, slip_id: int) -> dict:
        now = time.time()

        # Проверка кэша
        if slip_id in self.cache:
            ts, data = self.cache[slip_id]
            if now - ts < self.cache_ttl:
                return data

        try:
            # Создаем клиент с таймаутом
            timeout = ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(
                        f"{self.base_url}/{slip_id}"
                    ) as response:
                        data = await response.text()
                        data = json.loads(data)
                        # Сохраняем в кэш
                        self.cache[slip_id] = (now, data)
                        return data
                        
                except ClientError as e:
                    # Обработка ошибок соединения/таймаута
                    raise Exception(f"Failed to get data: {str(e)}")
                    
        except Exception as e:
            # Обработка других исключений
            raise Exception(f"Unexpected error occurred: {str(e)}")
