import telebot

from logic import BotLogic


with open(".secret", 'r') as f:
    secret = f.read()[:-1]
bot = telebot.TeleBot(secret)
logic = BotLogic(bot)


@bot.message_handler(content_types=['text']) 
def handle(message): 
    logic.process_message(message)

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
