import telebot
import os
import requests
import use
import re
import numpy as np
import time
token = '1304469910:AAEAZdGl2lcdKCa4PggTdPyckP-BscCObxs'
oleg_data_folder = 'oleg_bot_data'
bot = telebot.TeleBot(token)

start_play_words = [
    'play',
    'game',
    'играть',
    'игру',
    'сыграть',
    'игра',
    'да'
]

def create_folders(client_id):
    client_folder = f'{oleg_data_folder}/{client_id}'
    if not os.path.exists(oleg_data_folder):
        os.mkdir(oleg_data_folder)
    if not os.path.exists(client_folder):
        os.mkdir(client_folder)

def check_game_status(client_id):
    game_data = f'{oleg_data_folder}/{client_id}/game_data/'
    # не играл
    if not os.path.exists(game_data):
        return 0
    # прошел тест
    elif os.path.exists(game_data + 'good.txt'):
        return 1
    # не прошел
    else:
        return -1

def save_text(client_id, data):
    client_folder = f'oleg_bot_data/{client_id}'
    with open(client_folder + '/test.txt', 'a') as log_file:
        log_file.write(data + '\n')

def if_starting_play(message):
    for i in start_play_words:
        if i in message:
            return True
    return False

def get_level(user_id):
    file_path = f'{oleg_data_folder}/{user_id}/game_data/good.txt'
    if os.path.exists(file_path):
        f = open(file_path, 'r')
        for line in f:
            print(line)
            if 'level:' in line:
                return line.split(':')[-1]
    return '-1'

def pass_initial_test(message):
    client_id = message.from_user.id
    user_answer = message.text
    if not re.search(r'\d? \d? \d?', user_answer):
        bot.reply_to(message, 'Ты ввел ответы не в верном формате!')
        return None
    user_answer = [int(elem) for elem in user_answer.split()]
    if np.sum(np.where(np.asarray(user_answer) == np.array([3, 3, 2]), 1, 0)) == 3:
        msg = bot.send_message(chat_id = client_id, text = f'Все верно!\n Продолжим?')
        f = open(f'{oleg_data_folder}/{client_id}/game_data/good.txt', 'w')
        f.write('level:3')
        bot.register_next_step_handler(msg, handler)
    else:
        msg = bot.send_message(chat_id = client_id, text = f'Что же, начнем с азов. Приступим прямо сейчас?')
        f = open(f'{oleg_data_folder}/{client_id}/game_data/good.txt', 'w')
        f.write('level:1')
        bot.register_next_step_handler(msg, handler)

def pass_exam(client_id):
    pass

def read_article(client_id):
    pass

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = ('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    print(file)

@bot.message_handler(commands=['help'])
def help(message):
    user_name = message.from_user.first_name
    client_id = message.from_user.id
    bot.send_message(chat_id = client_id, text = f'Привет, Дорогой. С чем тебе помочь, что случилось?')

@bot.message_handler(commands=['start'])
def begin(message):
    user_name = message.from_user.first_name
    client_id = message.from_user.id
    create_folders(client_id)
    bot.send_message(chat_id = client_id, text = f'Привет, {user_name}!\nМеня зовут Олег')
    # 1) помочь с продуктами тинькоффа
    # 2) поиграть

def get_initial_test(client_id):
    time.sleep(3)
    with open('./test_test.txt', 'r', encoding= 'UTF-8') as f:
        lines = f.readlines()
        questions = [line.split(';') for line in lines]
        for i, q in enumerate(questions[:-1]):
            text_question = (
                f'Вопрос {i+1}. {q[0]}\n' 
                f'1. {q[1]}\n'
                f'2. {q[2]}\n'
                f'3. {q[3]}\n')
            msg = bot.send_message(chat_id = client_id, text = text_question)
@bot.message_handler(content_types=['text'])
def handler(message):
    print(message)
    client_id = message.from_user.id
    user_message = message.text

    if if_starting_play(user_message):
        if check_game_status(client_id) == 0:
            bot.send_message(chat_id = client_id, text = f'В начале тебе нужно пройти входной тест.')
            os.mkdir(f'{oleg_data_folder}/{client_id}/game_data')
            
            get_initial_test(client_id);
            bot.send_message(chat_id = client_id, text = 'Пример ввода при ответе на 3 вопроса: 1 2 3')
            msg = bot.send_message(client_id, "Удачи!", reply_markup=use.button_zero)
            bot.register_next_step_handler(msg, pass_initial_test)
        elif check_game_status(client_id) == 1:
            bot.send_message(chat_id = client_id, text = f'Твой уровень: {get_level(client_id)}.')
            bot.send_message(message.chat.id, "Выбор за тобой", reply_markup=use.button_first)
        else:
            msg = bot.send_message(chat_id = client_id, text = f'Ты еще даже не пытался пройти тест. Дерзай!')
            get_initial_test(client_id);
            bot.register_next_step_handler(msg, pass_initial_test)

    else:
        #save_text(client_id, user_message)
        bot.send_message(chat_id=client_id, text='Не обрабатываю все подряд.')

@bot.callback_query_handler(func=lambda call: True)    
def continue_game(call):

    if call.data == 'continue':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Начнем!")
            test = bot.send_message(call.message.chat.id, "Чем займёмся?", reply_markup=use.button_second)
    if call.data == 'test':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой ответ:")
        # bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
    if call.data == 'read':
        bot.send_message(call.message.chat.id, "Приятного изучения материала")
        to_read = 'Про самозанятость  https://journal.tinkoff.ru/news/npd-19-regionov/'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=to_read)
        bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)

    if call.data == 'exam':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой экзамен, удачи!!!")
        bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
    if call.data == "back":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назад")
        bot.send_message(call.message.chat.id, "Чем займёмся?", reply_markup=use.button_first)
    if call.data == "back2":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назад")
        bot.send_message(call.message.chat.id, "Выбор за тобой", reply_markup=use.button_second)


if __name__ == '__main__':
    bot.polling(none_stop=True)
