def main():
    # register command handlers
    from . import commands

    from .bot import updater

    # start bot
    updater.start_polling()

if __name__ == '__main__':
    main()