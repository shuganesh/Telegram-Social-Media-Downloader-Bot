import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import wget

from urllib.parse import urlparse

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)
options = []


def gen_markup():
  markup = InlineKeyboardMarkup()
  markup.row_width = 2
  markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
             InlineKeyboardButton("No", callback_data="cb_no"))
  return markup


# @bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: True)
def greet(message):
  if (checkLink(message.text)):
    stripedLink = checkLink(message.text)
    if (stripedLink == 'www.youtube.com'):
      facebookDownload(message.text)
    bot.send_message(message.chat.id, stripedLink, reply_markup=gen_markup())


def checkLink(link):
  domain = urlparse(link).netloc
  return domain


def facebookDownload(link):
  wget.download(link, '/filedir')


bot.polling()
