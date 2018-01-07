from .bot import bot


@bot.error
def errors_handler(bot, update, error):
    print(error)