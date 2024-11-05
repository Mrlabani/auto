from flask import Flask, request
from telegram import Bot, Update
import os
import time
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DELETE_DELAY = 10  # Seconds delay for message deletion
bot = Bot(token=BOT_TOKEN)

def delete_message(chat_id, message_id):
    time.sleep(DELETE_DELAY)
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)

    # Process messages in group chats only
    if update.message and update.message.chat.type in ["group", "supergroup"] and not update.message.from_user.is_bot:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

        # Run the deletion as a separate thread
        Thread(target=delete_message, args=(chat_id, message_id)).start()

    return 'ok'

@app.route('/')
def index():
    return "Telegram Bot is running!"

if __name__ == "__main__":
    app.run()
