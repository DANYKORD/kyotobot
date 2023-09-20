import telebot
import webbrowser
from telebot import types

# assign token to var
bot = telebot.TeleBot('6406707049:AAE4aPHKzlaafzZ_yjNlnvhw1uenB_Oq4DM')


# decorator to interact with /start can put other commands also
@bot.message_handler(commands=['start'])  # commanads in telegram on which execute main()
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Who is gay?')
    btn2 = types.KeyboardButton('David Gay')
    btn3 = types.KeyboardButton('David not a gay!')
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, f'Hi! {message.from_user.first_name}', reply_markup=markup)
    # to use buttons register func
    bot.register_next_step_handler(message, on_click)
def on_click(message):
    if message.text == 'Who is gay?':
        bot.send_message(message.chat.id, 'David for sure')
    elif message.text == 'David Gay':
        bot.send_message(message.chat.id, 'For sure')
    elif message.text == 'David not a gay!':
        bot.send_message(message.chat.id, 'DAVID LOVE BIG COCKS')

@bot.message_handler(commands=['file'])  # commanads in telegram on which execute main()
def file(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Nice photo')
    markup.add(btn1)
    file = open('./Astro.png', 'rb')
    # same for video audio etc
    bot.send_photo(message.chat.id, file, reply_markup=markup )
    # to use buttons register func
    bot.register_next_step_handler(message, on_click)
def on_click(message):
    if message.text == 'Nice photo':
        bot.send_message(message.chat.id, '❤️')

@bot.message_handler(commands=['help'])
def main(message):
    # format msg using html tags
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, f'Hi! {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID {message.from_user.id}')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://hackscope.net')


# buttons
@bot.message_handler(content_types=['photo', 'video'])
def get_content(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Open website', url='https://hackscope.net')
    btn2 = types.InlineKeyboardButton('Delete photo', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Edit text', callback_data='edit')
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.reply_to(message, 'What a beautiful photo!', reply_markup=markup)


# this method process callback_data
# create anonymous func if empty return true
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        # message_id current msg
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


# execute code unstoppable
# or bot.infinity_polling()
bot.polling(none_stop=True)
