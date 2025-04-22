import telebot
import requests

TELEGRAM_TOKEN = '7654233284:AAGa4eUxud9SiA1gcfIXfYgLBCfZsALobfQ'
OPENROUTER_API_KEY = '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'

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

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Oops! I'm feeling shy right now. Try again later."

@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    user_msg = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    ai_reply = talk_to_ai(user_msg)

    try:
        bot.send_message(
            chat_id=message.chat.id,
            text=ai_reply,
            reply_to_message_id=message.message_id
        )
    except Exception as e:
        print("Error sending reply:", e)
        bot.send_message(message.chat.id, ai_reply)  # fallback: send without reply

print("Bot is running...")
bot.polling()
