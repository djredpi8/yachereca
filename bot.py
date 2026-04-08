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

# Состояние: сколько нажатий сделал пользователь в текущем цикле
user_clicks: defaultdict[int, int] = defaultdict(int)

# Последовательность текста кнопки (то, что отправляет пользователь)
CLICK_TEXTS = [
    "Я хочу ящерицу!",   # 1 нажатие
    "Ящерица!",          # 2 нажатие
    "Ящерицу!",          # 3 нажатие
    "Ящерица",           # 4 нажатие
    "Ящерица",           # 5 нажатие
]


def make_keyboard(button_text: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text)]],
        resize_keyboard=True,
    )


async def silent_keyboard_update(message: types.Message, button_text: str) -> None:
    """Обновляет кнопку без видимого ответа: служебное сообщение сразу удаляется."""
    temp = await message.answer("\u2060", reply_markup=make_keyboard(button_text))
    await bot.delete_message(chat_id=temp.chat.id, message_id=temp.message_id)


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] = 0

    await message.answer(
        f"Ну давай, {user_name}, выбирай.",
        reply_markup=make_keyboard(CLICK_TEXTS[0]),
    )


@dp.message(F.text.in_(CLICK_TEXTS))
async def click_flow(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] += 1
    click_number = user_clicks[user_id]

    if click_number == 1:
        # Бот НЕ отвечает
        await silent_keyboard_update(message, CLICK_TEXTS[1])

    elif click_number == 2:
        await message.answer("Ящерица!", reply_markup=make_keyboard(CLICK_TEXTS[2]))
        await message.answer(f"{user_name}, может все таки хомячка?")

    elif click_number == 3:
        # Бот НЕ отвечает
        await silent_keyboard_update(message, CLICK_TEXTS[3])

    elif click_number == 4:
        # Бот НЕ отвечает
        await silent_keyboard_update(message, CLICK_TEXTS[4])

    elif click_number == 5:
        await message.answer("Ящерица", reply_markup=make_keyboard(CLICK_TEXTS[0]))
        await message.answer(f"{user_name}, ты дурак совсем?")
        user_clicks[user_id] = 0

    else:
        user_clicks[user_id] = 0
        await message.answer("Сброс цикла. Нажми кнопку снова.", reply_markup=make_keyboard(CLICK_TEXTS[0]))


async def main() -> None:
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
