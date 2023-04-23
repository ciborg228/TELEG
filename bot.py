import telebot
import sqlite3
from telebot import types
from config import bot

text = []


@bot.message_handler(commands=['dobavlenie'])
def application(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))

    msg = bot.send_message(message.chat.id, "Желаете зарегестрироваться?",
                           reply_markup=rmk)
    bot.register_next_step_handler(msg, user_answer)


def user_answer(message):
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, "Впишите ваши данные")
        bot.register_next_step_handler(msg, user_reg)
    elif message.text == "нет":
        bot.send_message(message.chat.id, "Без регистрации вы не сможете добавить свою историю")
    else:
        bot.send_message(message.chat.id, "Я что-то не понимаю вашей речи")


def user_reg(message):
    bot.send_message(message.chat.id, f"Your data: {message.text}")
    pmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pmk.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))

    mpg = bot.send_message(message.chat.id, "Желаете добавить свою историю?",
                           reply_markup=pmk)
    bot.register_next_step_handler(mpg, user_history)


def user_history(message):
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
    print(message.text)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, " Здравствуйте, приветствую Вас здесь. "
                          "Бот пока что создаётся, и его основные команды: "
                          "/info и /dobavlenie. ")


@bot.message_handler(commands=['info'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')

    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, 'Желаете узнать небольшую информацию о вас?',
                     reply_markup=markup_inline
                     )


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id = types.KeyboardButton("МОЙ ID")
        item_username = types.KeyboardButton("МОЙ НИК")

        markup_reply.add(item_id, item_username)
        bot.send_message(call.message.chat.id, "Нажмите на то, что вы бы хотели узнать",
                         reply_markup=markup_reply
                         )
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, "ну и иди далеко, и на долго")

# следующая функция показ айди и ника
# Показываетс он средством двух кнопок, которые находятся внизу панели
# конпка: МОЙ ID, показывает ваш ID, вауууу
#кнопка: МОЙ НИК, показывает вашь ник
@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == "МОЙ ID":
        bot.send_message(message.chat.id, f"ваш айди: {message.from_user.id}")
    elif message.text == 'МОЙ НИК':
        bot.send_message(message.chat.id, f"ваш ник: {message.from_user.first_name} {message.from_user.last_name}")


bot.polling()
