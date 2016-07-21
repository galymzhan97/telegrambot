import telebot
import config
import main



bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def analyze_strings(message):
    stringForAnalyze = message.text.encode('utf-8')
    result = main.apply_string(stringForAnalyze)
    bot.send_message(message.chat.id, result)

if __name__ == '__main__':
    bot.polling(none_stop=True)
