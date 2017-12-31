from telegram.ext import Filters

from .bot import message


@message(Filters.command)
def unknown_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command."
    )
