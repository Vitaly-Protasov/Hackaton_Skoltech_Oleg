import telebot
import os

token = #
oleg_data_folder = 'oleg_bot_data'
bot = telebot.TeleBot(token)
passed_initial_test = False
start_play_words = [
    'play',
    'game',
    'играть',
    'игру',
    'сыграть',
    'игра'
]

def create_folders(client_id):
    client_folder = f'{oleg_data_folder}/{client_id}'
    if not os.path.exists(oleg_data_folder):
        os.mkdir(oleg_data_folder)
    if not os.path.exists(client_folder):
        os.mkdir(client_folder)

def if_first_play(client_id):
    game_data = f'{oleg_data_folder}/{client_id}/game_data'
    return not os.path.exists(game_data)

def save_text(client_id, data):
    client_folder = f'oleg_bot_data/{client_id}'
    with open(client_folder + '/test.txt', 'a') as log_file:
        log_file.write(data + '\n')

def if_start_play(message):
    for i in start_play_words:
        if i in message:
            return True
    return False

@bot.message_handler(commands=['start'])
def begin(message):
    user_name = message.from_user.first_name
    client_id = message.from_user.id
    create_folders(client_id)
    bot.send_message(chat_id = client_id, text = f'Привет, {user_name}!\nМеня зовут Олег')
    bot.send_message(chat_id = client_id, text = f'Чем сегодня займемся?')
    # 1) помочь с продуктами тинькоффа
    # 2) поиграть

@bot.message_handler(content_types=['text'])
def handler(message):
    print(message)
    client_id = message.from_user.id
    user_message = message.text

    if if_start_play(user_message):
        if if_first_play(client_id):
            bot.send_message(chat_id = client_id, text = f'Ты еще не играл со мной.\nДавай пройдём входной тест')
            os.mkdir(f'{oleg_data_folder}/{client_id}/game_data')

            # pass_initial_test()
        else:
            bot.send_message(chat_id = client_id, text = f'Твой уровень: N. Место в лидерборде X')
            bot.send_message(chat_id = client_id, text = f'Выбор: читать статью или пройти экзамен по теме.')
    else:
        save_text(client_id, user_message)
        bot.send_message(chat_id=client_id, text='Done.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
