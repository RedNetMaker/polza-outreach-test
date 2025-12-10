# polza-outreach-test
Тестовое задание для Polza Outreach Engine: валидация email-доменов, интеграция с Telegram и архитектура email-аутрича

## Инструкция по запуску

### Требования
- Python 3.7 или выше
- pip

### Установка

1. Клонируйте репозиторий или перейдите в директорию проекта:
   ```bash
   cd polza-outreach-test
   ```

2. Создайте виртуальное окружение (если еще не создано):
   ```bash
   python -m venv venv
   ```

3. Активируйте виртуальное окружение:
   
   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (CMD):**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```

4. Установите зависимости:
   ```bash
   pip install -r email_validator/requirements.txt
   pip install -r telegram_sender/requarements.txt
   ```

## Задание 1: Валидация email-доменов

Запустите скрипт с email-адресами в качестве аргументов:

```bash
python email_validator/main.py email1@example.com email2@test.com
```

Если аргументы не указаны, скрипт использует тестовые данные по умолчанию:
```bash
python email_validator/main.py
```

## Задание 2: Интеграция с Telegram

**Примечание:** Используется тестовый Telegram-бот с тестовым токеном. Адрес бота: [@polza_testwork_bot](https://t.me/polza_testwork_bot)

### Режим 1: Сбор chat_id

Запустите бота в режиме прослушивания:
```bash
cd telegram_sender
python main.py listen
```

Бот ожидает команду `/start` от пользователей и сохраняет их `chat_id` в `chat_ids.json`.

### Режим 2: Отправка сообщений

1. Создайте файл `text.txt` с текстом сообщения
2. Запустите скрипт:
```bash
python main.py send
```

Скрипт отправляет текст из `text.txt` всем пользователям из `chat_ids.json`.

## Задание 3: Архитектура email-аутрича

Описание архитектуры системы для обслуживания 1200 email-адресов с мультитенантностью, ротацией адресов и высокой отказоустойчивостью находится в файле `task3/architecture.md`.