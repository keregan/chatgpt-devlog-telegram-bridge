# ChatGPT DevLog Telegram Bridge

Backend-сервис для публикации devlog-постов из ChatGPT в Telegram-канал через собственный API.

Проект работает как мост между Custom GPT и Telegram: пользователь пишет devlog-пост в ChatGPT, GPT Action вызывает API сервиса, FastAPI проверяет доступ, форматирует сообщение и отправляет его в Telegram через бота.

---

## Возможности

- Приём структурированных devlog-постов через API.
- Предпросмотр поста без отправки в Telegram.
- Публикация постов в Telegram-канал.
- Проверка доступа через секретный заголовок `x-bridge-token`.
- Форматирование постов в единый читаемый стиль.
- Интеграция с Telegram Bot API.
- Запуск приложения в Docker.
- Управление сервисами через Docker Compose.
- Reverse proxy через Caddy.
- HTTPS через автоматические TLS-сертификаты Caddy.
- OpenAPI-схема для подключения Custom GPT Action.
- GitHub Actions CI для проверки проекта.
- Pytest-тесты для логики форматирования.
- Healthcheck endpoint для проверки состояния сервиса.
- Docker healthcheck для контроля состояния контейнера.

---

## Как это работает

Общая схема:

```text
Custom GPT
   ↓
GPT Action
   ↓
HTTPS API endpoint
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
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── config.py
│   └── telegram_sender.py
├── tests/
│   └── test_format_devlog.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Caddyfile
├── Dockerfile
├── docker-compose.yml
├── openapi-actions.yaml
├── requirements.txt
└── README.md
```

---

## API endpoints

### Health check

```http
GET /health
```

Проверяет, что сервис запущен и отвечает.

Пример ответа:

```json
{
  "status": "ok",
  "service": "chatgpt-devlog-telegram-bridge"
}
```

Docker Compose также использует healthcheck, поэтому состояние контейнера можно проверить командой:

```bash
docker compose ps
```

Ожидаемый статус приложения:

```text
Up ... (healthy)
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
git clone git@github.com:your-username/chatgpt-devlog-telegram-bridge.git
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

Swagger будет доступен локально:

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

## Использование на сервере

Если проект планируется использовать не только локально, а как внешний API для Custom GPT Action, его нужно разместить там, где ChatGPT сможет обратиться к нему по публичному HTTPS-адресу.

Для этого понадобится:

- арендовать VPS/VDS или подготовить собственный сервер;
- установить Docker и Docker Compose;
- настроить `.env` с токенами Telegram и секретным ключом API;
- приобрести или подключить домен;
- направить DNS-запись домена на IP-адрес сервера;
- настроить Caddy как reverse proxy;
- получить HTTPS-сертификат через Caddy;
- указать публичный HTTPS-адрес в настройках GPT Action.

Зачем нужен сервер:

- сервис должен быть доступен постоянно, а не только пока включён локальный компьютер;
- Custom GPT Action должен иметь возможность отправить HTTP-запрос к API;
- Telegram-публикация должна работать из внешнего окружения;
- Docker-контейнеры должны стабильно работать в фоне.

Зачем нужен домен:

- домен даёт понятный постоянный адрес для API;
- через домен проще подключить HTTPS;
- Caddy может автоматически получить TLS-сертификат;
- GPT Action удобнее настраивать на стабильный HTTPS endpoint;
- при смене сервера можно обновить DNS, не меняя всю конфигурацию клиента.

В публичном репозитории не нужно указывать настоящий production-домен. Для примеров используется placeholder:

```text
https://your-domain.example
```

---

## Production deployment

Production-окружение может состоять из двух контейнеров:

```text
chatgpt-devlog-telegram-bridge
caddy
```

- `chatgpt-devlog-telegram-bridge` — FastAPI backend.
- `caddy` — reverse proxy и HTTPS.

Публичный `Caddyfile` в репозитории содержит только пример домена:

```caddy
your-domain.example {
    reverse_proxy chatgpt-devlog-telegram-bridge:8000
}
```

Для реального сервера рекомендуется использовать локальный файл:

```text
Caddyfile.local
```

Пример локального файла:

```caddy
your-real-domain.example {
    reverse_proxy chatgpt-devlog-telegram-bridge:8000
}
```

В `docker-compose.yml` можно подключать локальный Caddy-конфиг так:

```yaml
./Caddyfile.local:/etc/caddy/Caddyfile:ro
```

`Caddyfile.local` не должен попадать в GitHub.

---

## Custom GPT Action

Для публикации постов прямо из ChatGPT используется Custom GPT Action.

Файл схемы:

```text
openapi-actions.yaml
```

В нём описаны действия:

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

Перед использованием в production нужно заменить примерный server URL на реальный HTTPS-адрес в настройках GPT Action, не в публичном репозитории.

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

В проекте используется защита API через header:

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
- не указывать настоящий production-домен в публичных файлах;
- не коммитить `Caddyfile.local`;
- при утечке токена сразу заменить его;
- для GitHub использовать SSH-ключи вместо постоянного ввода токена.

Локальные и временные файлы должны игнорироваться Git:

```text
.env
*.bak
*.backup
*.local
Caddyfile.local
```

---

## Git workflow

Обычный процесс работы:

```bash
git status
git add app/main.py docker-compose.yml README.md
git commit -m "feat: update project"
git push origin main
```

Для подключения к GitHub можно использовать SSH:

```text
git@github.com:your-username/chatgpt-devlog-telegram-bridge.git
```

---

## Что реализовано

- FastAPI backend.
- Endpoint `/health`.
- Endpoint `/preview-devlog`.
- Endpoint `/publish-devlog`.
- Форматирование devlog-постов.
- Отправка сообщений в Telegram.
- Обработка ошибок Telegram API.
- Защита через `x-bridge-token`.
- Dockerfile.
- Docker Compose.
- Docker healthcheck.
- Caddy reverse proxy.
- HTTPS.
- Деплой на сервер.
- OpenAPI-схема для GPT Action.
- Интеграция с Custom GPT.
- GitHub Actions CI.
- Pytest-тесты.
- SSH push в GitHub.

---

## Текущий статус

Проект находится в рабочем состоянии.

Готово:

- API работает;
- Telegram-публикация работает;
- Custom GPT Action работает;
- HTTPS работает;
- Caddy проксирует запросы во FastAPI-контейнер;
- контейнер приложения имеет статус `(healthy)`;
- CI проходит;
- тесты проходят;
- публичный репозиторий очищен от production-значений.
