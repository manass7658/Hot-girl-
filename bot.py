import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def talk_to_ai(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a romantic, caring, flirty and loyal girlfriend who deeply understands her partner and expresses love freely."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Oops! I'm feeling shy right now. Try again later."

@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    user_msg = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    ai_reply = talk_to_ai(user_msg)
    bot.reply_to(message, ai_reply)

print("Bot is running...")
bot.polling()
