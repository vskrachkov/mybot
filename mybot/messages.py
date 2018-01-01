from telegram import ext

from .bot import bot


@bot.message(ext.Filters.command)
def unknown_msg(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command."
    )