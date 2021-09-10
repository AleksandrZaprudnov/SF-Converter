import telebot
from config import TOKETN, keys
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKETN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для конвертации валюты ' \
'введите строку (через пробелы), в бесплатной версии доступна только Евро:\n' \
'<В какую валюту> ' \
'<Значение конвертируемой валюты (цена)>\n' \
'Список доступных валют: /values'

    bot.reply_to(message, text)

@bot.message_handler(commands=['dict', 'values'])
def dictionary(message: telebot.types.Message):
    text = 'Список валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))

    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    try:
        prm = message.text.split(' ')

        if len(prm) != 2:
            raise ConvertionException('Количество параметров не соответсвует правилу конвертации')

        quote, amount = prm

        total_base = CryptoConverter.convert(quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка в исходных данных:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка выполнения\n{e}')
    else:
        text = f'Цена {amount} Евро в {quote} = {float(total_base) * float(amount)}'

        bot.send_message(message.chat.id, text)

bot.polling()
