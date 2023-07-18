import time
from pyrogram import Client, filters
import openai

# Создаем экземпляр клиента Pyrogram и передаем ему параметры авторизации
app = Client(
    "my_user_bot",
    api_id=api_id,  # Замените на свой api_id
    api_hash="api_hash"  # Замените на свой api_hash
)

openai.api_key = 'token'

model_running = False

# Ваш идентификатор пользователя (user_id)
your_user_id = yourid

# Словарь для отслеживания идентификаторов сообщений
message_ids = {}


# Регистрируем обработчик сообщений
@app.on_message(filters.command(["start", "stop"]) & filters.private)
def handle_commands(client, message):
    global model_running

    if message.from_user.id != your_user_id:
        return

    command = message.command[0].lower()

    if command == "start":
        if not model_running:
            model_running = True
            response = "Модель ChatGPT запущена."
        else:
            response = "Модель ChatGPT уже запущена."
    elif command == "stop":
        if model_running:
            model_running = False
            response = "Модель ChatGPT остановлена."
        else:
            response = "Модель ChatGPT уже остановлена."
    else:
        return

    # Отправляем ответное сообщение в чат
    client.send_message(chat_id=message.chat.id, text=response)


# Регистрируем обработчик обычных сообщений
@app.on_message(filters.text & filters.private)
def handle_message(client, message):
    global model_running

    if not model_running:
        return

    # Отправляем сообщение пользователя модели ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt='Тебя зовут BBL представь что ты умный авто ответчик' + message.text,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text.strip()

    client.send_message(chat_id=message.chat.id, text=f'🤖 Ответ BBL-Ответчика \n\n: {response}')


# Запускаем чат-бота
app.run()
