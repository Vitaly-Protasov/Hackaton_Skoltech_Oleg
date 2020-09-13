import telebot
import use

bot = telebot.TeleBot('1308010873:AAFp1erpp6AA8eDru3M1bLhtCuxnFDbBmiA')
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Привет, ты написал мне')
    
@bot.message_handler(content_types=["text"])
def start(message):

    bot.send_message(message.chat.id, "Привет, продолжим игру?", reply_markup=use.button_first)
    #bot.edit_message_reply_markup(message.chat.id, message_id = KeyboardMessageID, reply_markup = None)
    
@bot.callback_query_handler(func=lambda call: True)    
def continue_game(call):
    
        
    if call.data == 'continue':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Начнем")
            test = bot.send_message(call.message.chat.id, "Чем займёмся?", reply_markup=use.button_second)
            #bot.send_message(call.message.chat.id, "" ,reply_markup=use.startend)
    if call.data == 'test':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот твой тест:")
        bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
    if call.data == 'read':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой текст, приятного чтения")
        bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
    if call.data == 'exam':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Твой экзам, удачи!!!")
        bot.send_message(call.message.chat.id, "Вернуться к началу" ,reply_markup=use.button_to_start)
    if call.data == "back":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назад")
        bot.send_message(call.message.chat.id, "Чем займёмся?", reply_markup=use.button_first)
    if call.data == "back2":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Назад")
        bot.send_message(call.message.chat.id, "Привет, продолжим игру?", reply_markup=use.button_second)
            
# @bot.message_handler(content_types=['text'])
# def cbreply(message):
#     if message.text == "back":
#         bot.send_message(message.chat.id, "Чем займёмся?", reply_markup=use.button_second)

#     elif message.text == "back2":
#         bot.send_message(message.chat.id, "Привет, продолжим игру?", reply_markup=use.button_first)
        

bot.polling(none_stop=True)