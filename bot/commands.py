from bot.bot import command


@command('start')
def start(bot, update):
    from pprint import pprint

    print('bot: ')
    pprint(vars(bot))

    print('message text: ', update.message.text)
    print('date: ', update.message.date)
    print('chat: ', vars(update.message.chat))
    print('photos list: ', update.message.photo)
    print('stickers: ', update.message.sticker)
    print('video: ', update.message.video)

    print('Full name: ',
          f'{update.message.chat.first_name} '
          f'{update.message.chat.last_name}')

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello i am your bot !"
    )
