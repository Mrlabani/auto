from flask import Flask, request
from telegram import Bot, Update
import os
import time
from threading import Thread

app = Flask(__name__)

# Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
DELETE_DELAY = 10  # Delay in seconds for message deletion
bot = Bot(token=BOT_TOKEN)

# Function to delete messages after a delay
def delete_message(chat_id, message_id):
    time.sleep(DELETE_DELAY)
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

# Webhook route to handle updates
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)

    # Process messages in group chats only
    if update.message and update.message.chat.type in ["group", "supergroup"] and not update.message.from_user.is_bot:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

        # Run the deletion as a separate thread to avoid delay in response
        Thread(target=delete_message, args=(chat_id, message_id)).start()

    return 'ok', 200

# Root route for health check
@app.route('/')
def index():
    return "Telegram Auto-Delete Bot is running!"

if __name__ == "__main__":
    app.run()
