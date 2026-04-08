# yachereca

Готовый Telegram-бот на `aiogram` с кнопкой **«Ящерица»** и циклическим сценарием ответов.

## Быстрый старт

1. Установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Создайте токен в BotFather и задайте переменную окружения:

```bash
export BOT_TOKEN="<ваш_токен>"
```

3. Запустите бота:

```bash
python bot.py
```

## Важно по безопасности

- Не храните токен в коде.
- Если токен уже попал в публичный доступ, **обязательно отзовите его** через BotFather (`/revoke`) и выпустите новый.
