import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import httpx
import time
import hashlib
import hmac
from app.config import settings  # Импортируем ваши настройки

# !!! Используйте реальный токен бота из ваших настроек !!!
BOT_TOKEN = settings.bot_token
BASE_URL = "https://zjjjk-77-79-170-232.a.free.pinggy.link"
API_URL = f"{BASE_URL}/auth/telegram-login"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def generate_telegram_auth_data(user: types.User):
    """
    Генерирует словарь данных для FastAPI, как если бы они пришли из Mini App.
    """
    data = {
        "id": user.id,
        "auth_date": int(time.time()),
        "first_name": user.first_name,
        "username": user.username
    }

    # Логика генерации хеша с использованием секретного ключа (Bot Token)
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items()) if v is not None])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    data["hash"] = hmac_hash
    return data


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """Обрабатывает команду /start и регистрирует пользователя в FastAPI."""
    user = message.from_user

    if user is None:
        await message.reply("Не удалось получить данные пользователя Telegram.")
        return

    # 1. Генерируем данные для отправки на наш API
    auth_payload = generate_telegram_auth_data(user)

    # 2. Отправляем запрос на FastAPI (через ngrok туннель)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=auth_payload)

            if response.status_code == 200:
                # Успех: FastAPI вернул токены
                tokens = response.json()
                await message.reply(
                    f"✅ **Успешно!** Вы авторизованы/зарегистрированы в системе.\n"
                    f"Ваш ID в БД: **{tokens['user']['id']}**"
                    f"tokens: **{tokens}**"
                )
            else:
                # Ошибка: Например, неверный хеш
                await message.reply(f"❌ Ошибка регистрации в API. Код: {response.status_code}")

        except httpx.ConnectError:
            await message.reply("❌ Не удалось подключиться к API. Проверьте ngrok и FastAPI сервер.")


async def main():
    """Запуск бота в режиме Long Polling."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())