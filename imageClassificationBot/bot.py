# import required libraries
import os
import telebot
import datetime
import requests
import urllib.request
import subprocess
import config

# setup bot with Telegram token from config
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

bot_text = '''
Bip-bop human,
I classify images using neural networks 🚀
Send me pictures, and I will classify them for you 🤟
'''

# store files in /tmp so storage does not get complete  
result_storage_path = 'tmp'

# Handles all text messages that contains the command '/start' 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, bot_text)

# Handles all photo messages
@bot.message_handler(content_types=['photo'])
def handle(message):
    log_request(message)
    image_name = save_image_from_message(message)
  
    # object recognition
    object_recognition_image(image_name)
    bot.send_photo(message.chat.id, open('data/darknet/predictions.jpg','rb'), 'Identified objects, if any! 👻')
  
    # image classification
    classification_list_result = classify_image(image_name)
  
    # send classification results
    output = 'The image classifies as:\n'
    for result in classification_list_result:
        output += result
    output += '\n🚀 Gimme more pics! 🚀'
    
    bot.reply_to(message, output)
    cleanup_remove_image(image_name);  
  
# ----------- Helper functions ---------------
def log_request(message):
    file = open('data/logs.txt', 'a') #append to file
    file.write("{0} - {1} {2} [{3}]\n".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id)) 
    print("{0} - {1} {2} [{3}]".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id))
    file.close() 
  
def get_image_id_from_message(message):
    # there are multiple array of images, check the biggest
    return message.photo[len(message.photo)-1].file_id

def save_image_from_message(message):
    cid = message.chat.id  
    image_id = get_image_id_from_message(message)
    bot.send_message(cid, '🔥 Analyzing image, be patient ! 🔥')
  
    # prepare image for downlading
    file_path = bot.get_file(image_id).file_path

    # generate image download url
    image_url = "https://api.telegram.org/file/bot{0}/{1}".format(config.TELEGRAM_TOKEN, file_path)
    print(image_url)
  
    # create folder to store pic temporary, if it doesnt exist
    if not os.path.exists(result_storage_path):
        os.makedirs(result_storage_path)
  
    # retrieve and save image
    image_name = "{0}.jpg".format(image_id)
    urllib.request.urlretrieve(image_url, "{0}/{1}".format(result_storage_path,image_name))
  
    return image_name;

def classify_image(image_name):
    # classify image -> https://pjreddie.com/darknet/imagenet/
    os.system('cd data/darknet && ./darknet classifier predict cfg/imagenet1k.data cfg/darknet19.cfg darknet19.weights ../../{0}/{1} > ../../{0}/results.txt'.format(result_storage_path, image_name)) 
  
    # retrieve classification results
    results_file = open("{0}/results.txt".format(result_storage_path),"r") 
    results = results_file.readlines()
    results_file.close()  
    return results
  
def object_recognition_image(image_name):
    # object recognition -> https://pjreddie.com/darknet/yolo/
    os.system('cd data/darknet && ./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights ../../{0}/{1}'.format(result_storage_path, image_name)) 
  
def cleanup_remove_image(image_name):
    os.remove('{0}/{1}'.format(result_storage_path, image_name))

if __name__ == '__main__':
    # run bot in loop
    bot.polling(none_stop=True)
