import telebot;
from telebot import apihelper

token = open("/home/ksi/tgtoken1").read().strip()
apihelper.proxy = {'https':'socks5://127.0.0.1:9050'}
bot = telebot.TeleBot(token);

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == "/cat":
        bot.send_message(message.from_user.id, "X")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
