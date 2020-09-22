import os
import time
import telebot
from telebot import types
from dynaconf import settings
import flask
from flask import Flask, request
from check import Data

server = Flask(__name__)


token = settings.TGTOKEN


bot = telebot.TeleBot(token)

print('bot start')

def send_log(message):
    info = {
        "usr_id": str(message.from_user.id),
        "tag": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "text": message.text
    }
    return info


@bot.message_handler(commands=['start'])
def send_welcome(message):
    check = Data.base(())
    ct = f"""
        Привет! Я слежу за сайтами Mystream для оповещении о падении.\n
        Команда для вывода всех команд нажмите /help \n
        Всего в базе {check} cайтов
        """
    bot.send_message(message.chat.id, ct)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    ct = """
        Доступные команды:\n
        /list - выводит всех владельцев сайтов\n
        /check - бот проходит по всем сайтам независимо от таймера\n
        /add - добавляет страницу (в процессе)\n
        /remove - удаляет страницу (в процессе)
        """
    bot.send_message(message.chat.id, ct)


@bot.message_handler(commands=['list'])
def list(message):
    info  = Data.owners(())
    owners = '\n'.join(map(str, info))
    ct = f'Владельцы сатов\n{owners}'
    bot.send_message(message.chat.id, ct)


@bot.message_handler(commands=['check'])
def check(message):
    print(f"{time.time()}: Rise /check[{message.chat.id}]")
    owners = Data.owners(())
    info = []
    for owner in owners:
        if len(Data.site_error((), owner)) == 0:
             continue
        else:
            sites = f'{owner}\n' + '\n'.join(map(str, Data.site_error((), owner)))
            info.append(sites)
    if info is None:
        text = "Все сайты в порядке"
    else:

        text = '\n'.join(map(str, info))
    bot.send_message(message.chat.id, text)



@server.route('/' + token, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format('uptimer', token))
    return "Hello from Heroku!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))