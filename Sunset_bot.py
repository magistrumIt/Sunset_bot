#Ass We Can          # Талисман кода



# Импорт библиотек
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from time import sleep as s


a = dt.today()     # Определенние переменных и списков
mas_t = [a.hour, a.minute, a.second]

bot = telebot.TeleBot('5600142537:AAHQmOyvP7wBlOOtLwqcHfcLApCHv-cBBN4') 
answer = ''
keyboard = types.InlineKeyboardMarkup()

callback_inline_button = ["timer_15m", "timer_30m", "timer_45m", "timer_1h", "timer_1h30m", "timer_2h"]
time_in_seconds = [900, 1800, 2700, 3600, 5400, 7200]
answer_timer = ["15 минут", "30 минут", "45 минут", "1 час(-а)", "1 час(-а) 30 минут", "2 часа(-ов)"]



def par_sunset():   #Функция для парсинга времени заката
    url = 'https://voshod-solnca.ru/sun/%D1%81%D0%B0%D0%BD%D0%BA%D1%82-%D0%BF%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')


    quotes = soup.find_all('div', class_='today-list__item-value')
            
    a = quotes[7]
            
    return(a.text)


def give_time():    #Функция для определения времени до заката
    a = par_sunset()
    b = ""
    mas_t_sunset = []

    for ch in a:
        if ch == ":": mas_t_sunset.append(int(b)); b = ""
        else: b += ch

    mas_t_sunset.append(int(b))

    a = dt.today()
    mas_t = [a.hour, a.minute, a.second]
    
    t = mas_t[0] * 3600 + mas_t[1] * 60 + mas_t[2]
    
    t_sunset = mas_t_sunset[0] * 3600 + mas_t_sunset[1] * 60 + mas_t_sunset[2]
    
    t_when = t_sunset - t
    
    if t_when < 0:
        return "Но сегодня закат уже был!"
    
    
    hour = t_when / 3600
    minutes = hour * 10 % 10 / 10 * 60
    hour = int(hour // 1)
    seconds = minutes * 10 % 10 / 10 * 60
    minutes = int(minutes // 1)
    seconds = int(seconds // 1)
    
    
    return f"Через {hour} ч {minutes} мин {seconds} сек"


def convert_in_sec():   #Функция для конвертации времени в секунды
    
    a = par_sunset()
    b = ""
    mas_t_sunset = []

    for ch in a:
        if ch == ":": mas_t_sunset.append(int(b)); b = ""
        else: b += ch

    mas_t_sunset.append(int(b))

    a = dt.today()
    mas_t = [a.hour, a.minute, a.second]
    
    t = mas_t[0] * 3600 + mas_t[1] * 60 + mas_t[2]
    
    t_sunset = mas_t_sunset[0] * 3600 + mas_t_sunset[1] * 60 + mas_t_sunset[2]
    
    return t_sunset - t



@bot.message_handler(commands=["start"]) # Функция по обработке команды /start
def start(message, res=False):
    
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Во сколько закат?")
    markup.add(item1)
    item2=types.KeyboardButton("Напомнить о закате за...")
    markup.add(item2)
    
    key_timer_15m = types.InlineKeyboardButton(text='15 минут', callback_data='timer_15m')
    keyboard.add(key_timer_15m)
    key_timer_30m = types.InlineKeyboardButton(text='30 минут', callback_data='timer_30m')
    keyboard.add(key_timer_30m)
    key_timer_45m = types.InlineKeyboardButton(text='45 минут', callback_data='timer_45m')
    keyboard.add(key_timer_45m)
    key_timer_1h = types.InlineKeyboardButton(text='1 час', callback_data='timer_1h')
    keyboard.add(key_timer_1h)
    key_timer_1h30m = types.InlineKeyboardButton(text='1 час 30 минут', callback_data='timer_1h30m')
    keyboard.add(key_timer_1h30m)
    key_timer_2h = types.InlineKeyboardButton(text='2 часа', callback_data='timer_2h')
    keyboard.add(key_timer_2h)
    
    bot.send_message(message.chat.id, "Привет! Я бот, который указывает время до заката", reply_markup=markup)



@bot.message_handler(content_types=["text"]) # Функция по обработке основных кнопок
def handle_text(message, res=False):
    global answer, keyboard

    if message.text.strip() == 'Во сколько закат?':
        answer = 'Закат будет в ' + par_sunset()
        bot.send_message(message.chat.id, answer)
        
        answer = give_time()
        
        bot.send_message(message.chat.id, answer)
        
    elif message.text.strip() == 'Напомнить о закате за...':
        answer = 'Выбери за сколько напомнить'
        
        key_timer_15m = types.InlineKeyboardButton(text='15 минут', callback_data='timer_15m')
        key_timer_30m = types.InlineKeyboardButton(text='30 минут', callback_data='timer_30m')
        key_timer_45m = types.InlineKeyboardButton(text='45 минут', callback_data='timer_45m')
        key_timer_1h = types.InlineKeyboardButton(text='1 час', callback_data='timer_1h')
        key_timer_1h30m = types.InlineKeyboardButton(text='1 час 30 минут', callback_data='timer_1h30m')
        key_timer_2h = types.InlineKeyboardButton(text='2 часа', callback_data='timer_2h')
        
        bot.send_message(message.chat.id, answer, reply_markup=keyboard)
        
    
    else:
        answer = "Нажимай пожалуйста на кнопки, иначе я тебя не понимаю!"
        bot.send_message(message.chat.id, answer)
        
    

@bot.callback_query_handler(func=lambda call: True) # Команда обработки инлайн кнопок 
def callback_worker(call,): # Функция по обработке инлайн кнопок 
    global answer

    if convert_in_sec() < 0:
        answer = "Сегодня закат уже был!"

    else:
        for i in range(6):
            if call.data == callback_inline_button[i] and convert_in_sec() < time_in_seconds[i]: 
                answer = f"До заката меньше {answer_timer[i]}!"

                
            elif call.data == callback_inline_button[i]:
                answer = "Хорошо, напомню"
                bot.send_message(call.message.chat.id, answer)
                
                s(convert_in_sec() - time_in_seconds[i])
                answer = f"До заката {answer_timer[i]}!"

    bot.send_message(call.message.chat.id, answer)



bot.polling(none_stop=True, interval=0) # Запуск бота