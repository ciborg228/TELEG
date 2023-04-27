import datetime as dt

import telebot
from telebot import types

from config import TOKEN

text = []
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['dobavlenie'])
def application(message):
    '''до использования бота, обязательно нужно зарегестрироваться
 регистрация может быть любой и создана для проверки живой ли человек
 бот не сможет ввести данные, и соответственно не будет спамить
 На вопрос желаете зарегестрироваться желатьно не вводить ваши логины и пороли
 на вопрос тоже можно ответить и да и нет'''
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))

    msg = bot.send_message(message.chat.id, "Желаете зарегестрироваться?",
                           reply_markup=rmk)
    bot.register_next_step_handler(msg, user_answer)


def user_answer(message):
    '''если вы ответили да
поздравляю, впишите логин или пароль
если нет, то он может вас предупредить
так же бот может вас не понять
но дл этого надо постараться'''
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, "Впишите ваши данные")
        bot.register_next_step_handler(msg, user_reg)
    elif message.text == "нет":
        bot.send_message(message.chat.id, "Без регистрации вы не сможете добавить свою историю")
    else:
        bot.send_message(message.chat.id, "Я что-то не понимаю вашей речи")


# снова базовый вопрос
def user_reg(message):
    bot.send_message(message.chat.id, f"Your data: {message.text}")
    pmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pmk.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))

    mpg = bot.send_message(message.chat.id, "Желаете добавить свою историю?",
                           reply_markup=pmk)
    bot.register_next_step_handler(mpg, user_history)


def user_history(message):
    '''тут вы уже можете вписать свою историю
если же у вас нет времени, то бот просто предложить написать в другой раз'''
    if message.text == "Да":
        mpg = bot.send_message(message.chat.id, "Впишите вашу историю")
        bot.register_next_step_handler(mpg, user_dobav)
    elif message.text == "нет":
        bot.send_message(message.chat.id, "{Хорошо, надеюсь вы найдёте время написать её")
    else:
        bot.send_message(message.chat.id, "Это точно история?")


def user_dobav(message):
    bot.send_message(message.chat.id, "ваша история, успешно добавлена(нет)")
    text.append(message.text)
    name = message.from_user.id
    print(name, '==', message.text)
    f = open(f"histori/{name}.txt", 'a', encoding='UTF8')
    print(f'{dt.datetime.now()}, {message.text}\n', file=f)
    f.close()


@bot.message_handler(commands=['start'])
def start(message):
    '''приветствие и ознакомление с ботом'''
    bot.reply_to(message, " Здравствуйте, приветствую Вас здесь. "
                          "Бот пока что создаётся, и его основные команды: "
                          "/info и /dobavlenie. "
                          "ну и /help, для удобства")
    idphoto = open('1550472288_1.jpg', 'rb')
    bot.send_photo(message.chat.id, photo=idphoto)


@bot.message_handler(commands=['help'])
def start(message):
    bot.reply_to(message, "нужна помощь?\n"
                          "я вам не помощник")


@bot.message_handler(commands=['info'])
def get_user_info(message):
    '''здесь задаётся основной вопрос
 на него можете ответить либо да либо нет'''
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')

    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Желаете узнать небольшую информацию о вас?',
                     reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    '''следующая функция показ айди и ника
    он задаёт вопрос, на который вы можете ответить да, или нет
    при согласии бот даёт выбор:
    Показывает две кнопки, которые находятся внизу панели
    конпка: МОЙ ID, показывает ваш ID, вауууу
    кнопка: МОЙ НИК, показывает вашь ник
    при отказе бот вас посылает'''
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id = types.KeyboardButton("МОЙ ID")
        item_username = types.KeyboardButton("МОЙ НИК")

        markup_reply.add(item_id, item_username)
        bot.send_message(call.message.chat.id, "Нажмите на то, что вы бы хотели узнать",
                         reply_markup=markup_reply
                         )
    elif call.data == 'no':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemi_id = types.KeyboardButton("Да")
        itemi_username = types.KeyboardButton("нет")

        markup_reply.add(itemi_id, itemi_username)
        bot.send_message(call.message.chat.id, "вам так сложно?",
                         reply_markup=markup_reply
                         )


if __name__ == '__main__':
    bot.polling(none_stop=True)


@bot.message_handler(content_types=['text'])
def get_text(message):
    '''после вашего выбора, бот выдаёт результат
результатом будет то, что вы спросили
например, если вы спросили МОЙ ID, то вам покажут вашь айди
а если вы спросили МОЙ НИК, то вам выдастся ник'''
    if message.text == "МОЙ ID":
        bot.send_message(message.chat.id, f"ваш айди: {message.from_user.id}")
    elif message.text == 'МОЙ НИК':
        bot.send_message(message.chat.id, f"ваш ник: {message.from_user.first_name} {message.from_user.last_name}")


@bot.message_handler(content_types=['text'])
def get_text2(message):
    '''после вашего выбора, бот выдаёт результат
результатом будет то, что вы спросили
например, если вы спросили МОЙ ID, то вам покажут вашь айди
а если вы спросили МОЙ НИК, то вам выдастся ник'''
    if message.text == "Да":
        bot.send_message(message.chat.id, "вы очень большой лентяй")
    elif message.text == 'нет':
        bot.send_message(message.chat.id, "вам не видно, но я смотрю на вас осуждаюше")


bot.polling()
#You_funny_history_bot