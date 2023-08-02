import telebot
from config import keys, TOKEN
from extensions import ConvertionException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Привет! Я бот, который конвертирует одну валюту в другую.\
\nЧтобы увидеть список валют, с которыми я работаю,\nжми /values. \
\n\nА чтобы начать работать, напиши мне команду в следующем формате:\
\n<имя валюты> <в какую влюту перевести> <количество> \
\n\nНапример: доллар рубль 50"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные сейчас валюты: "
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Ты что-то не то написал, проверь.")

        quote, base, amount = values
        total_base = MoneyConverter.convert(quote, base, amount) * float(amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не могу обработать команду.\n{e}")
    else:
        text = f"Итак, переводим {quote} в {base}.\n{amount} {quote} = {total_base} {base}"
        bot.send_message(message.chat.id, text)


bot.infinity_polling()
