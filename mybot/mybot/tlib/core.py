from telegram import ext

__all__ = ['Bot', ]

class Bot:
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

    def command(self, command_name, *args, **kwargs):
        """Decorator that wraps handler for `command_name`.

        :param command_name: name of the command that handler will process
        """
        def wrapper(handler):
            assert callable(handler)
            command_handler = ext.CommandHandler(
                command_name, handler, *args, **kwargs)
            self.ds.add_handler(command_handler)
            return command_handler

        return wrapper

    def message(self, message_filter, *args, **kwargs):
        """Decorator that wraps handler for `message_filter`.

        :param message_filter: one of the possible filters
            from `telegram.ext.Filters` object
        """
        def wrapper(handler):
            message_handler = ext.MessageHandler(
                message_filter, handler, *args, **kwargs)
            self.u.dispatcher.add_handler(message_handler)
            return message_handler

        return wrapper

    def inline(self, handler, *args, **kwargs):
        """Decorator that register inline query handler.

        :param handler: callable that process user inline query
        """
        inline_handler = ext.InlineQueryHandler(
            handler, *args, **kwargs)
        self.ds.add_handler(inline_handler)
        return inline_handler

    def job(self, interval=60, first=0, repeating=False, once=False):
        """Decorator for register periodic task.

        :param interval: seconds interval between tasks or
            time to task execution if task register to run only once
        :param first: pause in seconds before first task
        :param repeating: run task repeatedly
        :param once: run task only once
        """
        # define default var for wrapper
        wrapper = None

        if once:
            # register job for only once performing
            def wrapper(handler):
                self.jq.run_once(handler, interval)

        elif repeating:
            # register job for repeatedly performing
            def wrapper(handler):
                job = self.jq.run_repeating(
                    handler, interval=interval, first=first
                )
                return job

        return wrapper

    def error(self, handler):
        """Decorator that wraps errors handler.

        :param handler: error handler
        """
        assert callable(handler), 'Error handler must be callable'
        self.ds.add_error_handler(handler)

    def run(self):
        self.u.start_polling()

    def start(self):
        self.run()

    def stop(self):
        self.u.stop()
