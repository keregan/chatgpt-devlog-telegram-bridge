# ChatGPT DevLog Telegram Bridge

Backend-сервис для публикации devlog-постов из ChatGPT в Telegram-канал.

Проект принимает готовый текст поста через защищённый API endpoint, проверяет секретный токен и отправляет сообщение в Telegram через Telegram Bot API.

---

## Описание проекта

ChatGPT DevLog Telegram Bridge создан как небольшой automation-сервис для ведения дневника разработки.

Основная идея проекта:

```text
ChatGPT формирует пост о выполненной работе
        ↓
backend принимает текст поста
        ↓
backend проверяет секретный токен
        ↓
Telegram-бот публикует пост в канал
```

Проект можно использовать для автоматизации публикаций о прогрессе разработки, учебных задачах, pet-проектах и DevOps-практике.

---

## Возможности

- приём POST-запросов через FastAPI
- защищённый endpoint для публикации постов
- проверка секретного токена через header
- отправка сообщений в Telegram-канал
- настройка через `.env`
- безопасное хранение токенов вне GitHub
- поддержка Telegram Bot API
- подготовка к будущей интеграции с ChatGPT Actions

---

## Статус проекта

✅ FastAPI backend создан  
✅ Endpoint `/publish-devlog` работает  
✅ Проверка secret token реализована  
✅ Telegram Bot подключён  
✅ Первый пост успешно опубликован в Telegram  
✅ Проект загружен на GitHub  

Текущая версия проекта работает локально.

---

## Структура проекта

```text
chatgpt-devlog-telegram-bridge/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── telegram_sender.py
│
├── logs/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Как работает проект

### 1. ChatGPT или другой клиент отправляет POST-запрос

Запрос отправляется на endpoint:

```text
POST /publish-devlog
```

В теле запроса передаётся текст поста:

```json
{
  "text": "День 29. Проект \"ChatGPT DevLog Telegram Bridge\"..."
}
```

---

### 2. Backend проверяет secret token

Для защиты endpoint используется header:

```text
x-bridge-token
```

Если токен неправильный, сервис возвращает ошибку:

```text
401 Invalid bridge token
```

---

### 3. Backend отправляет сообщение в Telegram

После успешной проверки сервис вызывает Telegram Bot API и публикует сообщение в указанный Telegram-канал.

---

## Используемые технологии

- Python
- FastAPI
- Uvicorn
- python-dotenv
- requests
- Telegram Bot API
- Git
- GitHub

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/keregan/chatgpt-devlog-telegram-bridge.git
cd chatgpt-devlog-telegram-bridge
```

---

### 2. Установить зависимости

```bash
python -m pip install -r requirements.txt
```

---

### 3. Создать `.env`

Создайте файл `.env` в корне проекта.

Пример содержимого:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=@your_telegram_channel
BRIDGE_SECRET_TOKEN=your_secret_token
```

---

## Переменные окружения

| Переменная | Описание |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота, полученный через BotFather |
| `TELEGRAM_CHAT_ID` | Username Telegram-канала или chat id |
| `BRIDGE_SECRET_TOKEN` | Секретный токен для защиты API endpoint |

Файл `.env` не должен попадать в GitHub.

---

## Запуск сервера

```bash
python -m uvicorn app.main:app --reload
```

После запуска сервер будет доступен по адресу:

```text
http://127.0.0.1:8000
```

---

## Проверка работы сервера

Откройте в браузере:

```text
http://127.0.0.1:8000
```

Ожидаемый ответ:

```json
{
  "status": "ok",
  "service": "ChatGPT DevLog Telegram Bridge"
}
```

---

## Документация API

FastAPI автоматически создаёт документацию:

```text
http://127.0.0.1:8000/docs
```

Через эту страницу можно проверить endpoint `/publish-devlog`.

---

## Пример отправки поста через PowerShell

```powershell
$headers = @{
    "x-bridge-token" = "test123"
}

$bodyObject = @{
    text = "День 29. Проект `"ChatGPT DevLog Telegram Bridge`"`n`nПодключаю Telegram-бота к backend-сервису для публикации devlog-постов.`n`n- backend принимает защищённые запросы`n- добавлена отправка сообщений в Telegram`n- проект начинает превращаться в связку ChatGPT → Telegram`n`nhttps://github.com/keregan/chatgpt-devlog-telegram-bridge"
}

$json = $bodyObject | ConvertTo-Json -Depth 10
$utf8Body = [System.Text.Encoding]::UTF8.GetBytes($json)

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/publish-devlog" `
    -Method Post `
    -Headers $headers `
    -Body $utf8Body `
    -ContentType "application/json; charset=utf-8"

$response | ConvertTo-Json -Depth 10
```

---

## Пример успешного ответа

```json
{
  "status": "ok",
  "post_preview": "День 29. Проект \"ChatGPT DevLog Telegram Bridge\"...",
  "telegram": {
    "status": "sent",
    "message": "Message sent to Telegram"
  }
}
```

---

## Безопасность

В проекте используется простой secret token для защиты endpoint.

Запрос должен содержать header:

```text
x-bridge-token: your_secret_token
```

Без правильного токена публикация невозможна.

Важно:

- не хранить реальные токены в коде
- не публиковать `.env` в GitHub
- использовать `.env.example` только как шаблон
- давать Telegram-боту только необходимые права

---

## Telegram-настройка

Для работы проекта нужно:

1. Создать бота через `@BotFather`
2. Получить Telegram Bot Token
3. Добавить бота администратором в Telegram-канал
4. Выдать боту право публиковать сообщения
5. Указать token и channel username в `.env`

Пример:

```env
TELEGRAM_CHAT_ID=@my_channel
```

---

## Текущие ограничения

На текущем этапе проект работает локально.

Адрес:

```text
http://127.0.0.1:8000
```

Такой адрес доступен только на локальном компьютере.

Для полноценной интеграции с ChatGPT Actions в будущем потребуется внешний HTTPS-адрес.

---

## Планы по развитию

Планируемые улучшения:

- добавить Dockerfile
- добавить Docker Compose
- добавить `openapi.yaml` для ChatGPT Actions
- подключить внешний HTTPS endpoint
- добавить preview-режим перед публикацией
- добавить логирование публикаций
- добавить историю отправленных постов
- добавить шаблоны постов
- добавить интеграцию с Git commit messages

---

## Цель проекта

Проект создаётся как практический backend/DevOps automation tool.

Он показывает навыки:

- создания REST API
- работы с FastAPI
- интеграции с внешним API
- безопасной работы с токенами
- настройки `.env`
- автоматизации публикаций
- подготовки сервиса к контейнеризации и дальнейшему deployment

---

## Версия

Текущая версия:

```text
v1.0 local
```

Основная локальная связка работает:

```text
FastAPI backend → Telegram Bot → Telegram Channel
```