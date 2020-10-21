from telegram.bot import bot
import telegram.messages as ms
import telegram.logics as logic
from base.check import Data



@bot.message_handler(commands=['start'])
def send_welcome(message):
    check = Data.base(())
    bot.send_message(message.chat.id, ms.WELCOME_MESSAGE(check))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, ms.HELP_MESSAGE)


@bot.message_handler(commands=['list'])
def list(message):
    bot.send_message(message.chat.id, logic.owners())


@bot.message_handler(commands=['check'])
def check(message):
    bot.send_message(message.chat.id, logic.export())


if __name__ == '__main__':
    bot.polling(none_stop=True)