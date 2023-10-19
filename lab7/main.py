import telebot
import config
from weeknow import curr_week_for_bd, curr_week
from execute import get_day_formatting, get_week_formatting

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, text="Здравствуйте, {0.first_name}! Я - бот для отображения информации о"
                                           " расписании. Напишите /help, чтобы понять, как я работаю"
                     .format(message.from_user))
    

@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(message.chat.id, text=config.help_txt)


@bot.message_handler(commands=['week'])
def help_bot(message):
    bot.send_message(message.chat.id, text=f'На данный момент {curr_week()} неделя')


@bot.message_handler(commands=['mtuci'])
def help_bot(message):
    bot.send_message(message.chat.id, text='Сайт МТУСИ: https://mtuci.ru')


@bot.message_handler(commands=['mon'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 1))}', parse_mode='HTML')


@bot.message_handler(commands=['tue'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 2))}', parse_mode='HTML')


@bot.message_handler(commands=['wed'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 3))}', parse_mode='HTML')


@bot.message_handler(commands=['thu'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 4))}', parse_mode='HTML')


@bot.message_handler(commands=['fr'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 5))}', parse_mode='HTML')


@bot.message_handler(commands=['sat'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_day_formatting(curr_week_for_bd(0), 6))}', parse_mode='HTML')


@bot.message_handler(commands=['curwk'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_week_formatting(curr_week_for_bd(0)))}', parse_mode='HTML')


@bot.message_handler(commands=['nxtwk'])
def mon(message):
    bot.send_message(message.chat.id, text=f'{str(get_week_formatting(curr_week_for_bd(1)))}', parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, text='Извините, я не понимаю')


bot.polling(none_stop=True, interval=0)
