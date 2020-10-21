import telebot
from dynaconf import settings

bot = telebot.TeleBot(settings.TGTOKEN)


