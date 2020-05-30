from telegram import Update
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from telegram.utils.request import Request
import config
import requests
from bs4 import BeautifulSoup as BS

# decorator for error
def log_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(f'Error: {ex}')
            raise ex
    return inner

@log_error
def welcome_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'anonymous'
    replyText = f'Hello, {name}!'
    update.message.reply_text(text=replyText)

@log_error
def help_handler(update: Update, context: CallbackContext):
    sti = open('static/stickers/help.webp', 'rb')
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=sti)
    
@log_error
def start_handler(update: Update, context: CallbackContext):
    sti = open('static/stickers/welcome.webp', 'rb')
    context.bot.send_sticker(chat_id=update.message.chat.id, sticker=sti)

@log_error
def f_handler(update: Update, context: CallbackContext):
    link = 'https://youtu.be/PZ8SxOQE0OA'
    update.message.reply_text(text=link)

@log_error
def weather_handler(update: Update, context: CallbackContext):
    r = requests.get('https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%B8%D0%B5%D1%80%D1%83%D1%81%D0%B0%D0%BB%D0%B8%D0%BC')
    tempMin = 'Not Found'
    tempMax = 'Not Found'
    text = 'Not Found'
    cityName = 'Not Found'

    soup = BS(r.content, 'html.parser')
    for el in soup.select('#content'):
        tempMin = el.select('.temperature .min')[0].text
        tempMax = el.select('.temperature .max')[0].text
        text = el.select('.wDescription .description')[0].text
    
    cityName = soup.find_all('strong')[0].get_text()
    
    context.bot.send_message(chat_id=update.message.chat.id, text="Привет, погода на сегодня "+cityName+":\n" +
        tempMin + ', ' + tempMax + '\n' + text)

@log_error
def main():
    print('Starting')
    # my request, per 0.5 sec
    req = Request(
        connect_timeout=0.5,
    )
    # bot for requests
    bot = Bot(
        request=req,
        token = config.TOKEN,
#        base_url="https://telegg.ru/orig/bot", # proxy
    )
    # updater get new data from telegram
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    print('I am your bot:', updater.bot.get_me())
    # only for /hello
    handlerHello = CommandHandler(command='hello', callback=welcome_handler)
    updater.dispatcher.add_handler(handlerHello)
    # only for /help
    handlerHelp = CommandHandler(command='help', callback=help_handler)
    updater.dispatcher.add_handler(handlerHelp)
    # only for /start
    handlerStart = CommandHandler(command='start', callback=start_handler)
    updater.dispatcher.add_handler(handlerStart)
    # only for f*ck
    handlerFck = MessageHandler(filters=Filters.text & Filters.regex('fuck'), callback=f_handler)
    updater.dispatcher.add_handler(handlerFck)
    # only for weather
    handlerFck = MessageHandler(filters=Filters.text & Filters.regex('weather'), callback=weather_handler)
    updater.dispatcher.add_handler(handlerFck)
    # download information from telegram
    updater.start_polling()
    # run bot in loop
    updater.idle()
    print('Finish')

if __name__ == '__main__':
    main()
