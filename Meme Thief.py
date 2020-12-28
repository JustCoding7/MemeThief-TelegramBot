# Comment the Platform's code you aren't using.
# Like if you are using Heroku then Comment every code written below #FOR PYTHONANYWHERE.
# Read Our Tutorials about how to deploy to know more.

import telebot
import time
import random
from flask import Flask, request
import os
import requests
from telebot import types as tp

# Setting up Bot #FOR HEROKU
TOKEN = '<token>'
WEBHOOK_URL = '<url>'
bot = telebot.TeleBot(TOKEN)

# Setting up Bot #FOR PYTHONANYWHERE
TOKEN = '<token>'
SECRET = '<secret>'
WEBHOOK_URL = '<url>' + SECRET
bot = telebot.TeleBot(TOKEN,threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# Stealing Memes
def getMeme():
    subs = ['memes','dankmemes','wholesomememes','blursedimages','cursedcomments','cursedimages','animemes','programmerhumor','holup','mandirgang']
    sub = random.choice(subs)
    response = requests.get(f"https://meme-api.herokuapp.com/gimme/{sub}").json()

    title = response.get(str('title'))
    plink = response.get(str('postLink'))
    subreddit = response.get(str('subreddit'))
    url = response.get(str('url'))

    return [title,plink,subreddit,url]

# Making Bot do something
@bot.message_handler(commands=['start','help'])
def info(message):
    '''Sends Start and Help Message.'''
    bot.send_message(message.chat.id,'Welcome to Meme Thief.\nThis bot provide you freshly stolen memes from Reddit.')

@bot.message_handler(commands=['denk'])
def Meme(message):
    memeData = getMeme()
    main = tp.InlineKeyboardMarkup(row_width=2)
    sub = tp.InlineKeyboardButton('Subreddit',url='https://www.reddit.com/r/{}/'.format(memeData[2]))
    post = tp.InlineKeyboardButton('PostLink',url=memeData[1])
    main.add(sub,post)

    bot.send_photo(message.chat.id,memeData[3],caption='*{}*'.format(memeData[0]),parse_mode='markdown',reply_markup=main)


# Setting up Web Hook #FOR HEROKU
app = Flask(__name__)
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL+ TOKEN)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# Setting up Web Hook #FOR PYTHONANYWHERE
app = Flask(__name__)
@app.route('/'+secret,methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok',200
