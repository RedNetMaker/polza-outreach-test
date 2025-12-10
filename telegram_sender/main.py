# Требования
#Принимает текст из файла .txt
#Отправляет в выбранный приватный Telegram-чат через бота
#UI не нужен
#Главное — чтобы работало

import sys
import json
import os
from telebot import TeleBot
from telebot.types import Message

BOT_TOKEN = "8494870449:AAGf8FN8xb3PGfsxMdnDamjjfpOgyUjBhqo"
CHAT_IDS_FILE = "chat_ids.json"

#1-й режим: Прослушивание и сбор chat_id из приватного чата
def listen_for_chat_id():
    print("Listening for chat_id...")
    bot = TeleBot(BOT_TOKEN)
    
    def load_chat_ids():
        """Загружает список chat_id из JSON файла"""
        if os.path.exists(CHAT_IDS_FILE):
            try:
                with open(CHAT_IDS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_chat_id(chat_id):
        """Сохраняет chat_id в JSON файл, если его там еще нет"""
        chat_ids = load_chat_ids()
        if chat_id not in chat_ids:
            chat_ids.append(chat_id)
            with open(CHAT_IDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(chat_ids, f, indent=2, ensure_ascii=False)
            print(f"Новый chat_id сохранен: {chat_id}")
            return True
        else:
            print(f"Chat_id уже существует: {chat_id}")
            return False
    
    @bot.message_handler(commands=['start'])
    def handle_start(message: Message):
        """Обработчик команды /start"""
        chat_id = str(message.chat.id)
        username = message.chat.username or "пользователь"
        first_name = message.chat.first_name or ""
        
        # Приветствие
        greeting = f"Привет, {first_name}! 👋\n\n"
        greeting += "Добро пожаловать! Ваш chat_id будет сохранен для дальнейшей работы."
        
        bot.reply_to(message, greeting)
        
        # Сохранение chat_id
        is_new = save_chat_id(chat_id)
        if is_new:
            bot.send_message(chat_id, f"✅ Ваш chat_id ({chat_id}) успешно сохранен!")
        else:
            bot.send_message(chat_id, f"ℹ️ Ваш chat_id ({chat_id}) уже был в базе.")
    
    print("Бот @polza_testwork_bot запущен и ожидает команду /start...")
    print("Нажмите Ctrl+C для остановки")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\nБот остановлен.")

#2-й режим: Отправка текста в выбранный приватный Telegram-чат через бота
def send_text_to_chat():
    """Читает text.txt и отправляет его содержимое всем chat_id из JSON"""
    TEXT_FILE = "text.txt"
    
    # Загрузка chat_ids из JSON
    def load_chat_ids():
        """Загружает список chat_id из JSON файла"""
        if os.path.exists(CHAT_IDS_FILE):
            try:
                with open(CHAT_IDS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка при чтении {CHAT_IDS_FILE}: {e}")
                return []
        return []
    
    # Проверка существования файла text.txt
    if not os.path.exists(TEXT_FILE):
        print(f"Ошибка: файл {TEXT_FILE} не найден!")
        return
    
    # Чтение текста из файла
    try:
        with open(TEXT_FILE, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print(f"Ошибка: файл {TEXT_FILE} пуст!")
            return
        
        print(f"Текст из {TEXT_FILE} загружен ({len(text)} символов)")
    except IOError as e:
        print(f"Ошибка при чтении {TEXT_FILE}: {e}")
        return
    
    # Загрузка chat_ids
    chat_ids = load_chat_ids()
    if not chat_ids:
        print(f"Ошибка: в файле {CHAT_IDS_FILE} нет chat_id!")
        return
    
    print(f"Найдено {len(chat_ids)} chat_id для отправки")
    
    # Инициализация бота
    bot = TeleBot(BOT_TOKEN)
    
    # Отправка сообщений
    success_count = 0
    error_count = 0
    
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id, text)
            print(f"✅ Сообщение отправлено в chat_id: {chat_id}")
            success_count += 1
        except Exception as e:
            print(f"❌ Ошибка при отправке в chat_id {chat_id}: {e}")
            error_count += 1
    
    print(f"\nИтого: успешно отправлено {success_count}, ошибок {error_count}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
        if text == "listen":
            listen_for_chat_id()
        elif text == "send":
            send_text_to_chat()
        else:
            print("Invalid command")
    else:
        print("Usage: python main.py <command>")