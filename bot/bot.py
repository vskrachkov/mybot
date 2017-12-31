import logging

from telegram.ext import Updater, CommandHandler, MessageHandler

__all__ = 'updater', 'log', 'command', 'message'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token='338265680:AAHPlTOyS91BFJ1mA_4xfHGoCoAngnVakj0')
log = logging.getLogger('bot')


def command(command_name):
    def wrapper(handler):
        assert callable(handler)
        command_handler = CommandHandler(command_name, handler)
        updater.dispatcher.add_handler(command_handler)
        return command_handler

    return wrapper


def message(message_filter):
    def wrapper(handler):
        message_handler = MessageHandler(message_filter, handler)
        updater.dispatcher.add_handler(message_handler)
        return message_handler

    return wrapper
