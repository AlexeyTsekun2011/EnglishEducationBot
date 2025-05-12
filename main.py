import json
import random
import telebot
from telebot import types
from config import TOKEN



bot = telebot.TeleBot(TOKEN)

try:
    with open("user_data.json", "r",encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

@bot.message_handler(commands=["start"])
def handle_start(message:types.Message):
    bot.send_message(message.chat.id,"Привет!")

@bot.message_handler(commands=["addword"])
def handle_addword(message:types.Message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(str(chat_id),{})
    try:
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
    except Exception as e:
        bot.send_message(chat_id,f"Произошла ошибка{e}")


@bot.message_handler(commands=["learn"])
def handle_learn(message:types.Message):
    bot.send_message(message.chat.id,"Начнём обучение")
    chat_id = message.chat.id
    user_dict = user_data.get(str(chat_id),{})
    if user_dict == {}:
        bot.send_message(chat_id,"У вас нет слов для изучения /addword")
        return

    try:
        words_number = int(message.text.split()[1])
        ask_translation(message.chat.id,user_dict,words_number)
    except ValueError:
        bot.send_message(chat_id,"Введите число слов которые вы хотите повторить /learn число")
    except IndexError:
        bot.send_message(chat_id,"Введите число слов которые вы хотите повторить /learn число")





def ask_translation(chat_id,user_words,words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id,f"Напишите перевод слова {word}")
        bot.register_next_step_handler_by_chat_id(chat_id,check_translation,translation,words_left)
    else:
        bot.send_message(chat_id,"Урок окончен!")




def check_translation(message,translation,words_left):
    try:
        user_translation = message.text.strip().lower()
        if user_translation == translation.lower():
            bot.send_message(message.chat.id,"Правильно!")
        else:
            bot.send_message(message.chat.id,f'Неправильно {translation}')
        words_left -= 1
        ask_translation(message.chat.id,user_data[str(message.chat.id)],words_left)
    except AttributeError:
        bot.send_message(message.chat.id,"Введите слово")
        ask_translation(message.chat.id,user_data[str(message.chat.id)],words_left)





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
