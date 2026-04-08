import asyncio
import os
from collections import defaultdict
from pathlib import Path

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, KeyboardButton, ReplyKeyboardMarkup

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

LIZARD_BUTTON_TEXT = "Ящерица"
RESTART_BUTTON_TEXT = "Сначала"

lizard_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=LIZARD_BUTTON_TEXT), KeyboardButton(text=RESTART_BUTTON_TEXT)]],
    resize_keyboard=True,
)

# Изображения по шагам:
# 1 -> /start (картинка 1),
# 2 -> после 1-го нажатия (картинка 2),
# 3 -> после 2-го нажатия (картинка 3),
# 4 -> после 3-го нажатия (картинка 4),
# 5 -> после 4-го нажатия (картинка 5).
IMAGE_PATHS = {
    1: Path("assets/image1.jpg"),
    2: Path("assets/image2.jpg"),
    3: Path("assets/image3.jpg"),
    4: Path("assets/image4.jpg"),
    5: Path("assets/image5.jpg"),
}


async def send_step_image(message: types.Message, image_index: int) -> None:
    image_path = IMAGE_PATHS[image_index]
    if image_path.exists():
        await message.answer_photo(FSInputFile(image_path))
    else:
        await message.answer(f"[Не найден файл изображения: {image_path}]")


async def start_flow(message: types.Message) -> None:
    user_id = message.from_user.id

    user_clicks[user_id] = 0

    await send_step_image(message, 1)
    await message.answer(
        "Ты можешь выбрать любого питомца, которого ты захочешь",
        reply_markup=lizard_keyboard,
    )


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await start_flow(message)


@dp.message(F.text == RESTART_BUTTON_TEXT)
async def restart_button(message: types.Message) -> None:
    await start_flow(message)


@dp.message(F.text == LIZARD_BUTTON_TEXT)
async def lizard_click(message: types.Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "друг"

    user_clicks[user_id] += 1
    step = user_clicks[user_id]

    if step == 1:
        await message.answer("Нуу не знаю, что тебе нравится")
        await send_step_image(message, 2)
        return

    if step == 2:
        await send_step_image(message, 3)
        return

    if step == 3:
        await send_step_image(message, 4)
        return

    if step == 4:
        await message.answer(f"{user_name}, ты дурак совсем?")
        await send_step_image(message, 5)
        user_clicks[user_id] = 0
        return

    # Защита от рассинхронизации
    user_clicks[user_id] = 0


async def main() -> None:
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
