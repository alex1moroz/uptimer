import telebot
import re
from check import Data
import time
from dynaconf import settings

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


# @bot.message_handler(content_types=['text'], commands=['add'])
# def send_text(message):
#     bot.send_message(message.chat.id, 'Добавьте автора и ссылку на страницу \nАвтор url')
#     data = re.match(r'\S+', message.text)
#     name = data.group(0)
#     url = data.group(1)
#     ask = f'Записываем следующие данные:\n{name} - автор страницы,\n{url} - ссылка на странцу'
#     bot.send_message(message.chat.id, ask)
#     bot.answer_callback_query()
#     if answer == "Да":
#         Data.add_row(author=name, url=url)
#
#     return author

bot.polling(none_stop=True, interval=0)