# ChatGPT DevLog Telegram Bridge

Backend-сервис для публикации devlog-постов из ChatGPT в Telegram-канал.

Проект принимает готовый текст поста через защищённый API endpoint и отправляет его в Telegram через Telegram Bot API.

## Возможности

- приём POST-запросов через FastAPI
- защита endpoint через секретный token
- отправка сообщений в Telegram-канал
- настройка через `.env`
- безопасное хранение токенов вне GitHub
- подготовка к интеграции с ChatGPT Actions

## Статус проекта

✅ FastAPI backend создан  
✅ Защищённый endpoint работает  
✅ Telegram Bot подключён  
✅ Первый пост успешно опубликован в Telegram  