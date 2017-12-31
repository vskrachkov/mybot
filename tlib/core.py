from telegram import ext

__all__ = ['T', ]

class T:
    """Class helper that hold a lot of helpers that must simplify
    development of the Telegram bot.

    :param token: yours bot token
    """
    def __init__(self, token):
        self._token = token
        self.u = ext.Updater(token=token)
        self.ds = self.u.dispatcher
        self.jq = self.u.job_queue

    @property
    def log(self):
        """Provide simple default logger. You can customize it by env vars.
        Env vars:
            :T_LOG_FORMAT: logger format
            :T_LOG_LEVEL: logger level
        """
        raise NotImplemented

    def command(self, command_name):
        """Decorator that wraps handler for `command_name`.

        :param command_name: name of the command that handler will process
        """
        ds = self.ds
        def wrapper(handler):
            assert callable(handler)
            command_handler = ext.CommandHandler(command_name, handler)
            ds.add_handler(command_handler)
            return command_handler

        return wrapper

    def message(self, message_filter):
        """Decorator that wraps handler for `message_filter`.

        :param message_filter: one of the possible filters
            from `telegram.ext.Filters` object
        """
        updater = self.u
        def wrapper(handler):
            message_handler = ext.MessageHandler(message_filter, handler)
            updater.dispatcher.add_handler(message_handler)
            return message_handler

        return wrapper

    def inline(self, handler):
        """Decorator that register inline query handler.

        :param handler: callable that process user inline query
        """
        inline_handler = ext.InlineQueryHandler(handler)
        self.ds.add_handler(inline_handler)
        return inline_handler

    def job(self, interval, first):
        """Decorator for register periodic task.

        :param interval: seconds interval between tasks
        :param first: pause in seconds before first task
        """
        raise NotImplemented

    def error(self, error):
        """Decorator that wraps error handler for the `error`.

        :param error: type of the error
        """
        raise NotImplemented

    def run(self):
        self.u.start_polling()

    def start(self):
        self.run()

    def stop(self):
        self.u.stop()
