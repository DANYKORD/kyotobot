import telebot
# pip install CurrencyConverter
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6406707049:AAE4aPHKzlaafzZ_yjNlnvhw1uenB_Oq4DM')
currency = CurrencyConverter()
amount = 0


# c.convert(100, 'EUR', 'USD')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, enter amount:')
    bot.register_next_step_handler(message, summ)


def summ(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Uncorrected format enter again:')
        bot.register_next_step_handler(message, summ)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Other', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Choose pairs:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Value must be bigger than 0, enter again:')
        bot.register_next_step_handler(message, summ)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id,
                         f'You will get: {round(res, 2)} {values[1]}. You can reenter again value:')
        bot.register_next_step_handler(call.message, summ)
    else:
        bot.send_message(call.message.chat.id, 'Enter pair (ex. usd/eur) :')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'You will get: {round(res, 2)} {values[1]}. You can reenter again value:')
        bot.register_next_step_handler(message, summ)
    except Exception:
        bot.send_message(message.chat.id, 'Something went wrong, please enter again (ex. usd/eur):')
        bot.register_next_step_handler(message, summ)

bot.polling(none_stop=True)
