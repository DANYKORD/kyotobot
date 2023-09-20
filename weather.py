import telebot
import requests
import json

bot = telebot.TeleBot('6406707049:AAE4aPHKzlaafzZ_yjNlnvhw1uenB_Oq4DM')
API = '9799032bea8d43825a7575232d735ffb'
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi, nice to see you, write your city: ')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200: # html page ok
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Now temperature at {city} is : {temp} С')

        image = 'sunny.png' if temp > 18.0 else 'cloudy.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'"{city}" Uncorrect please send again : ')

bot.polling(none_stop=True)