# ChatGPT DevLog Telegram Bridge

Backend-сервис для публикации devlog-постов из ChatGPT в Telegram-канал.

Проект работает как мост между Custom GPT и Telegram: пользователь пишет devlog-пост в ChatGPT, GPT Action вызывает API сервиса, FastAPI форматирует сообщение и отправляет его в Telegram через бота.

Проект сделан как практический backend/DevOps-проект: с Docker, VPS-деплоем, HTTPS, Caddy, GitHub Actions, тестами и OpenAPI-схемой для GPT Action.

---

## Что умеет проект

- Принимать структурированные devlog-посты через API.
- Делать preview поста без отправки в Telegram.
- Публиковать посты в Telegram-канал.
- Проверять доступ через секретный заголовок `x-bridge-token`.
- Форматировать посты в единый стиль.
- Работать через HTTPS-домен.
- Запускаться в Docker.
- Использовать Caddy как reverse proxy.
- Автоматически проверяться через GitHub Actions.
- Подключаться к Custom GPT через OpenAPI-схему.

---

## Как это работает

Общая схема:

```text
Custom GPT
   ↓
GPT Action
   ↓
https://your-domain.example
   ↓
Caddy reverse proxy
   ↓
FastAPI container
   ↓
Telegram Bot API
   ↓
Telegram channel
```

Пользователь пишет в Custom GPT, например:

```text
Опубликуй devlog: сегодня добавил CI и тесты. Теги: DevOps, FastAPI, Telegram.
```

GPT Action вызывает endpoint `/publish-devlog`, сервис проверяет токен, форматирует пост и отправляет сообщение в Telegram.

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
- GitHub Actions
- Pytest
- OpenAPI schema
- Custom GPT Actions

---

## Структура проекта

```text
chatgpt-devlog-telegram-bridge/
├── app/
│   ├── main.py
│   ├── config.py
│   └── telegram_sender.py
├── tests/
│   └── test_format_devlog.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Caddyfile
├── Dockerfile
├── docker-compose.yml
├── openapi-actions.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## API endpoints

### Health check

```http
GET /
```

Проверяет, что сервис запущен.

Пример ответа:

```json
{
  "status": "ok",
  "service": "ChatGPT DevLog Telegram Bridge"
}
```

---

### Preview devlog

```http
POST /preview-devlog
```

Создаёт предпросмотр поста, но не отправляет его в Telegram.

Header:

```http
x-bridge-token: your_secret_token
```

Request body:

```json
{
  "title": "Preview endpoint",
  "content": "Добавлен endpoint предпросмотра devlog-поста без отправки в Telegram.",
  "tags": ["FastAPI", "Backend", "DevOps"]
}
```

Response:

```json
{
  "status": "ok",
  "post_preview": "🚀 Preview endpoint\n\nДобавлен endpoint предпросмотра devlog-поста без отправки в Telegram.\n\n#FastAPI #Backend #DevOps"
}
```

---

### Publish devlog

```http
POST /publish-devlog
```

Форматирует и отправляет devlog-пост в Telegram-канал.

Header:

```http
x-bridge-token: your_secret_token
```

Request body:

```json
{
  "title": "GPT Action для публикации в Telegram",
  "content": "Сегодня подключил OpenAPI-схему для GPT Action, чтобы ChatGPT мог отправлять devlog-посты напрямую в Telegram-канал.",
  "tags": ["DevOps", "ChatGPT", "FastAPI", "Telegram"]
}
```

Пример результата в Telegram:

```text
🚀 GPT Action для публикации в Telegram

Сегодня подключил OpenAPI-схему для GPT Action, чтобы ChatGPT мог отправлять devlog-посты напрямую в Telegram-канал.

#DevOps #ChatGPT #FastAPI #Telegram
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

Описание:

| Переменная | Назначение |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота |
| `TELEGRAM_CHAT_ID` | ID Telegram-канала или чата |
| `BRIDGE_SECRET_TOKEN` | Секретный токен для защиты API |

Файл `.env` не должен попадать в GitHub.

---

## Локальный запуск

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

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

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

Swagger будет доступен здесь:

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

## Production deployment

Production-версия развёрнута на VPS и доступна через HTTPS:

```text
https://your-domain.example/docs
```

В production используется:

- Ubuntu VPS
- Docker
- Docker Compose
- FastAPI
- Caddy
- HTTPS
- Telegram Bot API

---

## Caddy

Caddy используется как reverse proxy и принимает внешние HTTP/HTTPS-запросы.

Пример `Caddyfile`:

```caddy
your-domain.example {
    reverse_proxy chatgpt-devlog-telegram-bridge:8000
}
```

Caddy автоматически получает TLS-сертификат и проксирует запросы во внутренний FastAPI-контейнер.

---

## Docker Compose services

В production работают два контейнера:

```text
chatgpt-devlog-telegram-bridge
caddy
```

- `chatgpt-devlog-telegram-bridge` — FastAPI backend.
- `caddy` — reverse proxy и HTTPS.

---

## Custom GPT Action

Для публикации постов прямо из ChatGPT используется Custom GPT Action.

Файл схемы:

```text
openapi-actions.yaml
```

В нём описаны два действия:

```text
previewDevlog
publishDevlog
```

### Настройка Action

В Custom GPT:

```text
Configure → Actions → Create new action
```

В поле Schema вставляется содержимое файла:

```text
openapi-actions.yaml
```

В Authentication выбирается:

```text
API Key
```

Тип ключа:

```text
Custom
```

Название header:

```text
x-bridge-token
```

В поле API key вставляется значение переменной:

```env
BRIDGE_SECRET_TOKEN
```

После настройки можно писать в Custom GPT:

```text
Сделай preview devlog-поста: сегодня добавил тесты и CI. Теги: DevOps, FastAPI, GitHub Actions.
```

или:

```text
Опубликуй devlog: сегодня подключил GPT Action для отправки постов в Telegram. Теги: DevOps, ChatGPT, Telegram.
```

---

## GitHub Actions CI

В проекте настроен базовый CI pipeline.

Файл:

```text
.github/workflows/ci.yml
```

CI запускается при push и pull request в ветку `main`.

Проверяется:

- установка зависимостей;
- синтаксис Python-файлов;
- импорт FastAPI-приложения;
- запуск тестов через pytest.

---

## Тесты

Тесты находятся в папке:

```text
tests/
```

Запуск тестов:

```bash
python -m pytest
```

В Docker-контейнере:

```bash
docker compose exec chatgpt-devlog-telegram-bridge python -m pytest
```

Сейчас тестируется форматирование devlog-постов:

- пост с тегами;
- пост без тегов;
- очистка и форматирование тегов.

---

## Безопасность

В проекте используется простая защита API через header:

```http
x-bridge-token
```

Если токен отсутствует или неверный, сервис возвращает:

```http
401 Unauthorized
```

Важно:

- не коммитить `.env`;
- не публиковать Telegram bot token;
- не вставлять секреты в README;
- при утечке токена сразу заменить его;
- для GitHub использовать SSH-ключи вместо постоянного ввода токена.

---

## Git workflow

Обычный процесс работы:

```bash
git status
git add app/main.py app/telegram_sender.py README.md
git commit -m "feat: update project"
git push origin main
```

Для подключения к GitHub используется SSH:

```text
git@github.com:keregan/chatgpt-devlog-telegram-bridge.git
```

---

## Что было реализовано

В рамках проекта реализовано:

- FastAPI backend;
- endpoint `/preview-devlog`;
- endpoint `/publish-devlog`;
- форматирование devlog-постов;
- отправка сообщений в Telegram;
- обработка ошибок Telegram API;
- защита через `x-bridge-token`;
- Dockerfile;
- Docker Compose;
- Caddy reverse proxy;
- HTTPS-домен;
- деплой на VPS;
- OpenAPI-схема для GPT Action;
- интеграция с Custom GPT;
- GitHub Actions CI;
- pytest-тесты;
- SSH push в GitHub.

---

## Текущий статус

Проект находится в рабочем production-ready состоянии.

Готово:

- API работает;
- Telegram-публикация работает;
- Custom GPT Action работает;
- HTTPS работает;
- CI проходит;
- тесты проходят;
- проект опубликован на GitHub.

---

## Возможные улучшения

Потенциальные следующие шаги:

- добавить retry-механику при временной недоступности Telegram;
- добавить structured logging;
- добавить endpoint для просмотра версии приложения;
- добавить Docker healthcheck;
- добавить автодеплой через GitHub Actions;
- добавить поддержку нескольких Telegram-каналов;
- добавить шаблоны постов;
- добавить changelog;
- добавить monitoring/uptime check.

---

## Автор

Проект создан как практический backend/DevOps-проект для изучения:

- FastAPI;
- Docker;
- деплоя на VPS;
- reverse proxy;
- HTTPS;
- CI/CD;
- тестирования;
- интеграции ChatGPT с внешним API;
- публикации сообщений в Telegram через GPT Action.
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
https://your-domain.example/docs
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
your-domain.example {
    reverse_proxy chatgpt-devlog-telegram-bridge:8000
}
```

Caddy принимает внешние запросы на домен `your-domain.example` и перенаправляет их во внутренний FastAPI-контейнер.

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
