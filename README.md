# ChatGPT DevLog Telegram Bridge

Сервис для публикации devlog-постов из ChatGPT в Telegram-канал.

Проект принимает структурированный HTTP-запрос с заголовком, текстом и тегами, форматирует его в читаемый пост и отправляет сообщение через Telegram Bot API.  
Основная цель проекта — автоматизировать публикацию заметок о ходе разработки и использовать сервис как небольшой production-ready backend-проект для практики DevOps, Docker, FastAPI и деплоя на VPS.

---

## О проекте

`ChatGPT DevLog Telegram Bridge` — это небольшой backend-сервис, который работает как мост между внешним клиентом и Telegram-каналом.

Сценарий использования:

1. Пользователь отправляет POST-запрос на API.
2. Сервис проверяет секретный токен в заголовке.
3. Получает данные devlog-поста: заголовок, содержание и теги.
4. Форматирует текст в единый стиль.
5. Отправляет готовое сообщение в Telegram-канал.

Проект развёрнут на VPS и доступен через домен с HTTPS.

---

## Возможности

- FastAPI backend
- Endpoint для публикации devlog-постов
- Проверка доступа через `x-bridge-token`
- Поддержка структурированного формата поста:
  - `title`
  - `content`
  - `tags`
- Автоматическое форматирование сообщения для Telegram
- Интеграция с Telegram Bot API
- Docker-контейнеризация
- Запуск через Docker Compose
- Reverse proxy через Caddy
- HTTPS через автоматические TLS-сертификаты
- Деплой на VPS
- Swagger-документация API

---

## Технологии

- Python
- FastAPI
- Pydantic
- Requests
- Telegram Bot API
- Docker
- Docker Compose
- Caddy
- Ubuntu VPS
- Git / GitHub
- SSH deploy workflow

---

## Архитектура

Общий принцип работы:

```text
Client / Swagger
        ↓
HTTPS request
        ↓
Caddy reverse proxy
        ↓
FastAPI container
        ↓
Telegram Bot API
        ↓
Telegram channel
```

В production-окружении приложение работает в Docker-контейнере.  
Caddy принимает внешние HTTP/HTTPS-запросы и проксирует их во внутренний FastAPI-сервис на порт `8000`.

---

## Структура проекта

```text
chatgpt-devlog-telegram-bridge/
├── app/
│   ├── main.py
│   ├── config.py
│   └── telegram_sender.py
├── Dockerfile
├── docker-compose.yml
├── Caddyfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Переменные окружения

Для работы проекта нужен файл `.env`.

Пример:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_channel_id
BRIDGE_SECRET_TOKEN=your_secret_bridge_token
```

Описание переменных:

| Переменная | Назначение |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота |
| `TELEGRAM_CHAT_ID` | ID Telegram-канала или чата |
| `BRIDGE_SECRET_TOKEN` | Секретный токен для защиты API |

Файл `.env` не должен попадать в GitHub.

---

## Запуск локально

### 1. Клонировать репозиторий

```bash
git clone git@github.com:keregan/chatgpt-devlog-telegram-bridge.git
cd chatgpt-devlog-telegram-bridge
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

### 3. Активировать окружение

Для Linux/macOS:

```bash
source .venv/bin/activate
```

Для Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

### 5. Создать `.env`

```bash
cp .env.example .env
```

После этого нужно заполнить значения переменных окружения.

### 6. Запустить приложение

```bash
uvicorn app.main:app --reload
```

Локальная документация API будет доступна по адресу:

```text
http://127.0.0.1:8000/docs
```

---

## Запуск через Docker Compose

```bash
docker compose up -d --build
```

Проверить контейнеры:

```bash
docker compose ps
```

Посмотреть логи:

```bash
docker compose logs --tail=100
```

Остановить проект:

```bash
docker compose down
```

---

## API

### Health Check

```http
GET /
```

Пример ответа:

```json
{
  "status": "ok",
  "service": "ChatGPT DevLog Telegram Bridge"
}
```

---

### Publish DevLog

```http
POST /publish-devlog
```

Заголовок:

```http
x-bridge-token: your_secret_bridge_token
```

Тело запроса:

```json
{
  "title": "Deployment complete",
  "content": "Проект успешно развернут на VPS через Docker, Caddy и HTTPS.",
  "tags": ["DevOps", "Docker", "FastAPI", "Telegram"]
}
```

Пример результата в Telegram:

```text
🚀 Deployment complete

Проект успешно развернут на VPS через Docker, Caddy и HTTPS.

#DevOps #Docker #FastAPI #Telegram
```

---

## Production deployment

Проект развёрнут на VPS и доступен через HTTPS:

```text
https://devlog.kereg.ru/docs
```

Production stack:

- Ubuntu VPS
- Docker
- Docker Compose
- FastAPI
- Telegram Bot API
- Caddy reverse proxy
- HTTPS

---

## Caddy

Caddy используется как reverse proxy.

Пример `Caddyfile`:

```caddy
devlog.kereg.ru {
    reverse_proxy chatgpt-devlog-telegram-bridge:8000
}
```

Caddy принимает внешние запросы на домен `devlog.kereg.ru` и перенаправляет их во внутренний FastAPI-контейнер.

---

## Docker Compose

В production используются два сервиса:

- `chatgpt-devlog-telegram-bridge` — FastAPI backend
- `caddy` — reverse proxy и HTTPS

Пример запуска:

```bash
docker compose up -d --build
```

---

## Безопасность

В проекте используется простой механизм защиты API через заголовок:

```http
x-bridge-token
```

Если токен не передан или передан неверно, API возвращает ошибку `401 Unauthorized`.

Важно:

- не хранить реальные токены в репозитории;
- не отправлять `.env` в GitHub;
- при случайной публикации токена — заменить его;
- для GitHub использовать SSH-ключи вместо постоянного ввода токена.

---

## Git workflow

Основные команды для работы с изменениями:

```bash
git status
git add app/main.py docker-compose.yml README.md
git commit -m "feat: update devlog bridge"
git push origin main
```

Для подключения к GitHub используется SSH:

```bash
git@github.com:keregan/chatgpt-devlog-telegram-bridge.git
```

---

## Текущий статус проекта

Проект находится в рабочем состоянии.

Реализовано:

- backend на FastAPI;
- публикация devlog-постов в Telegram;
- защита endpoint через секретный токен;
- поддержка структурированных постов;
- Docker-сборка;
- Docker Compose;
- деплой на VPS;
- домен;
- HTTPS;
- reverse proxy через Caddy;
- push на GitHub через SSH.

---

## Планы по развитию

Возможные следующие улучшения:

- добавить логирование успешных и неуспешных отправок;
- сделать более понятные ответы при ошибках Telegram API;
- добавить retry-механику при временной недоступности Telegram;
- добавить шаблоны постов;
- добавить поддержку нескольких Telegram-каналов;
- добавить endpoint для предпросмотра поста без отправки;
- добавить GitHub Actions для проверки проекта;
- добавить тесты для форматирования devlog-постов.

---

## Автор

Проект создан как практический DevOps/backend-проект для изучения:

- FastAPI;
- Docker;
- деплоя на VPS;
- reverse proxy;
- HTTPS;
- интеграции с внешними API;
- GitHub workflow.
