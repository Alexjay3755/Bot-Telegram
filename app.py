import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену на которую Вы хотите узнать> \
    \n<имя валюты, в которой нужно указать цену первой валюты>\n<количество первой валюты>   Например:\n"доллар рубль 1"\
    \nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Колличество параметров не равно 3.')

        base, quote, amount = values
        total_base = CryptoConverter.convert(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена за {amount} {base} в {quote} - {round(total_base * float(amount),2)}'
        bot.send_message(message.chat.id, text)


bot.polling()