import config
import apiai, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token=config.TOKEN)
dispatcher = updater.dispatcher

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello, let\'s talk?')

def textMessage(bot, update):
    request = apiai.ApiAI(config.TOKEN_Small_Talk).text_request() # Token API to Dialogflow
    request.lang = 'en-US' # In what language will the request be sent
    request.session_id = 'BatlabAIBot' # Session ID is required (you need to learn the bot later)
    request.query = update.message.text # send a request to the AI with a message from the user
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # parse JSON and pull out the answer
    # If there is an answer from the bot - send it to the user, if not - the bot did not understand it
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='I do not quite understand you!')

# Handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Add handlers to dispatcher
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Start search updates
updater.start_polling(clean=True)

# stop the bot if it was clicked Ctrl + C
updater.idle()
