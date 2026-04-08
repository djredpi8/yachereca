import asyncio
import os
from collections import defaultdict

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "Переменная окружения BOT_TOKEN не установлена. "
        "Создайте токен через BotFather и запустите: BOT_TOKEN=... python bot.py"
    )

bot = Bot(token=TOKEN)
dp = Dispatcher()

# В памяти процесса: user_id -> number of clicks in current cycle
user_clicks: defaultdict[int, int] = defaultdict(int)

lizard_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ящерица")]],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] = 0

    await message.answer(
        f"Ну давай, {user_name}, выбирай.",
        reply_markup=lizard_button,
    )


@dp.message(F.text == "Ящерица")
async def lizard_button_press(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] += 1
    clicks = user_clicks[user_id]

    if clicks == 1:
        await message.answer("Я хочу ящерицу")
    elif clicks == 2:
        await message.answer("Ящерица")
    elif clicks == 3:
        await message.answer("Ящерица")
        await message.answer(f"Может хомячка, {user_name}?")
    elif clicks == 4:
        await message.answer("Ящерица")
    elif clicks == 5:
        await message.answer("Я хочу ящерицу")
        await message.answer(f"{user_name}, ты дурак совсем какая ящерица")
        user_clicks[user_id] = 0
    else:
        user_clicks[user_id] = 0
        await message.answer("Я хочу ящерицу")


async def main() -> None:
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
