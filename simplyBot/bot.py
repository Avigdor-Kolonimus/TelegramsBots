import telebot 
from telebot import types
import config
import random

bot = telebot.TeleBot(config.TOKEN)

# Handles all text messages that contains the command '/start' 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    sti = open('static/stickers/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Random number")
    item2 = types.KeyboardButton("😊 How are you?")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Welcome, <i>{0.first_name}</i>!\nMy name <b>{1.first_name}</b> and I am bot!".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

# Handles all text messages that contains the command '/help'
@bot.message_handler(commands=['help'])
def send_dweeb(message):
    sti = open('static/stickers/help.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "<b>{0.first_name}</b> is dweeb!".format(message.from_user), parse_mode='html')

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    text = 'interesting'
    bot.reply_to(message, text)

# Handles all text messages that match the regular expression
@bot.message_handler(regexp="[1]")
def handle_message(message):
    text = 'Saitama is the main protagonist of One-Punch Man and the most powerful being to exist in the series.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Random number':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == '😊 How are you?':
 
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Good", callback_data='good')
            item2 = types.InlineKeyboardButton("Bad", callback_data='bad')
 
            markup.add(item1, item2)
 
            bot.send_message(message.chat.id, 'Excellent and you?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'I do not know what to answer 😢')
            bot.send_message(message.chat.id, 'Listen to my favorite opening 😊')
            # sendAudio
            audio = open('static/music/myLikeMusic.mp3', 'rb')
            bot.send_audio(message.chat.id, audio, 'hehe', 'eternnoir', 'My favorite opening')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "That's great 😊")
                # show alert
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="I am Batman")
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'It happens 😢')
                # show alert
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="I am Batman")
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 How are you?", reply_markup=None)
 
    except Exception as e:
        print(repr(e))

if __name__ == '__main__':
    # run bot in loop
    bot.polling(none_stop=True)
