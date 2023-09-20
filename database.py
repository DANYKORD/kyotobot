import telebot
import sqlite3

bot = telebot.TeleBot('6406707049:AAE4aPHKzlaafzZ_yjNlnvhw1uenB_Oq4DM')
name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()
# create table: users , with : id, name , password
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit() # synch above command with file
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Hello! Enter username: ')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter password:')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))   #id is autoincrement
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('List of Users', callback_data='users'))
    bot.send_message(message.chat.id, 'User registered', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True) # lambda - return true if no parametr
def callback(call):
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users') # choise all fields
    # no need commit - commit for delete asdd etc
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Name: {el[1]}, Password: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)