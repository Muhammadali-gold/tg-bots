import telebot
from telebot import types

bot = telebot.TeleBot("1069336438:AAG2ZREqTRBTGlI1nSan5QXykDUJU2-xKxM", parse_mode="HTML")


@bot.message_handler(commands=['start', 'helps'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    print("echo-all")
    print(message)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
#     bot.reply_to(message, "bu hazil")
#     print("echo-all")
#     print(message)


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
# else:
#     bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
GAME_NOT_STARTED = 0
GAME_STARTED = 1
GUESSED_LESS = 2
GUESSED_LARGER = 4
GUESSED_CORRECT = 8
GUESSED_ENDED = 16


class GuessInt:
    def __init__(self):
        self.status = None
        self.thoughtNum = None
        self.steps = 0

    def start(self):
        self.status = GAME_STARTED
        self.refresh()

    def guess(self, gueesedInt):
        self.steps += 1
        if gueesedInt == self.thoughtNum:
            self.status = GUESSED_CORRECT
        elif gueesedInt > self.thoughtNum:
            self.status = GUESSED_LARGER
        else:
            self.status = GUESSED_LESS

    def refresh(self):
        import random
        self.status = GAME_NOT_STARTED
        self.thoughtNum = random.randint(1, 99)
        self.steps = 0


name = ''
surname = ''
age = 0
game: GuessInt = GuessInt()


@bot.message_handler(content_types=['text'])
def start(message):
    # if message.text == '/reg':
    #     bot.send_message(message.from_user.id, "Как тебя зовут?")
    #     bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    # else:
    #     bot.send_message(message.from_user.id, 'Напиши /reg')
    if message.text == '/startGame':
        print("game started")
        game.start()
        bot.reply_to(message, "Game started. Good luck!\nStart to guess.")
    elif game.status != GAME_NOT_STARTED:
        guess = message.text
        print(f"player guessed = {guess}")
        if check_int(guess):
            game.guess(int(guess))
            if game.status == GUESSED_CORRECT:
                bot.reply_to(message, f"Congratulation. You guessed correctly in {game.steps} steps")
            if game.status == GUESSED_LESS:
                bot.reply_to(message, "You guessed integer is less than my thought number")
            if game.status == GUESSED_LARGER:
                bot.reply_to(message, "You guessed integer is larger than my thought number")
        else:
            bot.reply_to(message, "Please enter integer type number")


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    # global age
    # while age == 0:  # проверяем что возраст изменился
    #     try:
    #         age = int(message.text)  # проверяем, что возраст введен корректно
    #     except Exception:
    #         bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    # bot.send_message(message.from_user.id, 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?')
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        pass  # .... #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        pass  # ... #переспрашиваем


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


bot.polling()
