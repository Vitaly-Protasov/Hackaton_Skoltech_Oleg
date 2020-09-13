import telebot
import os
import requests
import use
import re
import numpy as np
import time

class OlegBot:
    def __init(self):
        self.token = ''
        self.oleg_data_folder = 'oleg_bot_data'
        self.start_play_words = [
                        'play',
                        'game',
                        'играть',
                        'игру',
                        'сыграть',
                        'игра',
                        'да'
                        ]
        self.bot = telebot.TeleBot(token)

    def _create_folders(self, client_id) -> None:
        client_folder = f'{self.oleg_data_folder}/{client_id}'
        if not os.path.exists(self.oleg_data_folder):
            os.mkdir(oleg_data_folder)
        if not os.path.exists(client_folder):
            os.mkdir(client_folder)

    def _check_game_status(self, client_id) -> number:
        game_data = f'{self.oleg_data_folder}/{client_id}/game_data/'
        # не играл
        if not os.path.exists(game_data):
            return 0
        # прошел тест
        elif os.path.exists(game_data + 'good.txt'):
            return 1
        # не прошел
        else:
            return -1

    def _if_starting_play(self, message) -> bool:
        for i in self.start_play_words:
            if i in message:
                return True
        return False

    def _get_level(self, user_id)-> str:
        file_path = f'{self.oleg_data_folder}/{user_id}/game_data/good.txt'
        if os.path.exists(file_path):
            f = open(file_path, 'r')
            for line in f:
                if 'level:' in line:
                    return line.split(':')[-1]
        return '-1'

    def _pass_initial_test(self, message) -> None:
        client_id = message.from_user.id
        user_answer = message.text
        if not re.search(r'\d? \d? \d?', user_answer):
            self.bot.reply_to(message, 'Ты ввел ответы не в верном формате!')
            return None
        user_answer = [int(elem) for elem in user_answer.split()]
        if np.sum(np.where(np.asarray(user_answer) == np.array([3, 3, 2]), 1, 0)) == 3:
            msg = bot.send_message(chat_id = client_id, text = f'Все верно!\n Продолжим?')
            f = open(f'{self.oleg_data_folder}/{client_id}/game_data/good.txt', 'w')
            f.write('level:3')
            self.bot.register_next_step_handler(msg, handler)
        else:
            msg = bot.send_message(chat_id = client_id, text = f'Что же, начнем с азов. Приступим прямо сейчас?')
            f = open(f'{self.oleg_data_folder}/{client_id}/game_data/good.txt', 'w')
            f.write('level:1')
            self.bot.register_next_step_handler(msg, handler)

    @bot.message_handler(content_types=['voice'])
    def voice_processing(self, message) -> str:
        file_info = bot.get_file(message.voice.file_id)
        file = ('https://api.telegram.org/file/bot{0}/{1}'.format(self.token, file_info.file_path))
        return file

    @bot.message_handler(commands=['help'])
    def help(self, message) -> None:
        user_name = message.from_user.first_name
        client_id = message.from_user.id
        self.bot.send_message(chat_id = client_id, text = f'Привет, Дорогой. С чем тебе помочь, что случилось?')

    @bot.message_handler(commands=['start'])
    def begin(self, message)  -> None:
        user_name = message.from_user.first_name
        client_id = message.from_user.id
        self.create_folders(client_id)
        self.bot.send_message(chat_id = client_id, text = f'Привет, {user_name}!\nМеня зовут Олег')
        # 1) помочь с продуктами тинькоффа
        # 2) поиграть

    def _get_initial_test(self, client_id) -> None:
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
                msg = self.bot.send_message(chat_id = client_id, text = text_question)
    @bot.message_handler(content_types=['text'])
    def handler(self, message) -> None:
        client_id = message.from_user.id
        user_message = message.text

        if self._if_starting_play(user_message):
            if self._check_game_status(client_id) == 0:
                self.bot.send_message(chat_id = client_id, text = f'В начале тебе нужно пройти входной тест.')
                os.mkdir(f'{self, oleg_data_folder}/{client_id}/game_data')
                
                self._get_initial_test(client_id);
                msg = bot.send_message(client_id, "Удачи!", reply_markup=use.button_zero)
                self.bot.register_next_step_handler(msg, self._pass_initial_test)
            elif self._check_game_status(client_id) == 1:
                self.bot.send_message(chat_id = client_id, text = f'Твой уровень: {self._get_level(client_id)}.')
                self.bot.send_message(chat_id = client_id, text = f'Выбор: читать статью или пройти экзамен по теме.')
                self.bot.send_message(message.chat.id, "Выбор за тобой", reply_markup=use.button_first)
            else:
                msg = bot.send_message(chat_id = client_id, text = f'Ты еще даже не пытался пройти тест. Дерзай!')
                self._get_initial_test(client_id);
                self.bot.register_next_step_handler(msg, pass_initial_test)

        else:
            #save_text(client_id, user_message)
            self.bot.send_message(chat_id=client_id, text='Не обрабатываю все подряд.')

    @bot.callback_query_handler(func=lambda call: True)    
    def continue_game(self, call):

        if call.data == 'continue':
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Начнем!")
                test = bot.send_message(call.message.chat.id, "Чем займёмся?", reply_markup=use.button_second)
        if call.data == 'test':
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой входной тест:")
            # bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
        if call.data == 'read':
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой текст, приятного чтения!")
            self.bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
        if call.data == 'exam':
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой экзамен, удачи!!!")
            self.bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
        if call.data == "back":
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назад")
            self.bot.send_message(call.message.chat.id, "Чем займёмся?", reply_markup=use.button_first)
        if call.data == "back2":
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назад")
            self.bot.send_message(call.message.chat.id, "Выбор за тобой", reply_markup=use.button_second)
