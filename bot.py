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

# Сколько раз пользователь нажал кнопку в текущем цикле
user_clicks: defaultdict[int, int] = defaultdict(int)

lizard_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ящерица")]],
    resize_keyboard=True,
)

# Ожидаемые реплики пользователя по шагам цикла (для логики сценария)
USER_STEP_TEXTS = {
    1: "Я хочу ящерицу!",
    2: "Ящерица!",
    3: "Ящерицу!",
    4: "Ящерица",
    5: "Ящерица",
}


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] = 0

    await message.answer(
        f"Ну давай, {user_name}, выбирай.",
        reply_markup=lizard_keyboard,
    )


@dp.message(F.text == "Ящерица")
async def lizard_click(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] += 1
    step = user_clicks[user_id]

    # 1, 3, 4 нажатия: бот не отвечает
    if step in {1, 3, 4}:
        return

    # 2 нажатие: бот отвечает
    if step == 2:
        await message.answer(f"{user_name}, может все таки хомячка?")
        return

    # 5 нажатие: бот отвечает и сбрасывает цикл
    if step == 5:
        await message.answer(f"{user_name}, ты дурак совсем?")
        user_clicks[user_id] = 0
        return

    # Защита от рассинхронизации: если > 5, сбрасываем
    user_clicks[user_id] = 0


async def main() -> None:
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
