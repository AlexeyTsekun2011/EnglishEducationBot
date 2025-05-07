import json
import random
import telebot
from telebot import types
from config import TOKEN



bot = telebot.TeleBot(TOKEN)

with open("user_data.json", "r",encoding="utf-8") as file:
    user_data = json.load(file)

@bot.message_handler(commands=["start"])
def handle_start(message:types.Message):
    bot.send_message(message.chat.id,"Привет!")

@bot.message_handler(commands=["addword"])
def handle_addword(message:types.Message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(str(chat_id),{})

    words = message.text.split()[1:]
    if len(words) == 2:
        word,translation = words[0].lower(),words[1].lower()
        user_dict[word] = translation
        user_data[str(chat_id)] = user_dict
        with open("user_data.json","w",encoding="utf-8") as file:
            json.dump(user_data,file,ensure_ascii=False,indent=4)
        bot.send_message(chat_id,"Слово добавлено")
    else:
        bot.send_message(chat_id,"Ошибка ввода")


@bot.message_handler(commands=["learn"])
def handle_learn(message:types.Message):
    chat_id = message.chat.id
    sadasd = user_data.get(str(chat_id),{})
    sadadasda = random.choice(sadasd)
    


    bot.send_message(message.chat.id,"Начнём обучение")


@bot.message_handler(commands=["help"])
def handle_help(message:types.Message):
    bot.send_message(message.chat.id,"Привет это пот на изучения английского языка\n"
                                     "/learn - для начала твоего обучения\n"
                                     "/start - запускает бота\n"
                                     "На этом пока все,скоро появятся новые функции!")

@bot.message_handler(func=lambda message:True)
def handle_all(message:types.Message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id,"У меня нет имени")
    elif message.text.lower() == "как у тебя дела?":
        bot.send_message(message.chat.id,"У меня всегда всё хорошо")
    elif message.text.lower() == "ты обучишь меня английскому?":
        bot.send_message(message.chat.id,"Конечно")





if __name__ == '__main__':
    bot.polling(none_stop=True)
