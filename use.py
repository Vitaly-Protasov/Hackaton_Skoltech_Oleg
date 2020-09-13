import telebot
types = telebot.types

button_zero = types.InlineKeyboardMarkup()
btn0 = types.InlineKeyboardButton(text="Начать тест", callback_data='test')
button_zero.row(btn0)

button_first = types.InlineKeyboardMarkup()
button_first.row_width = 1
btn1 = types.InlineKeyboardButton(text="Продолжить игру", callback_data='continue')
button_first.row(btn1)

button_second = types.InlineKeyboardMarkup()
button_second.row_width = 2
btn2 = types.InlineKeyboardButton(text="Изучить материал", callback_data='read')
btn3 = types.InlineKeyboardButton(text="Сдать экзамен по теме", callback_data='exam')
btn4 = types.InlineKeyboardButton(text="Назад", callback_data='back')
list_of_buttons = [btn2, btn3, btn4]
for btn in list_of_buttons:
    button_second.add(btn)

button_to_start = types.InlineKeyboardMarkup()
btn5 = types.InlineKeyboardButton(text="Назад", callback_data='back2')
button_to_start.row(btn5)
