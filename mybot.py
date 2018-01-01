from telegram import (
    ext, InlineQueryResultArticle, InputTextMessageContent
)

from tlib import T

t = T(token='338265680:AAHPlTOyS91BFJ1mA_4xfHGoCoAngnVakj0')


@t.command('start')
def start(bot, update):
    from pprint import pprint

    print('bot: ')
    pprint(vars(bot))

    print('message text: ', update.message.text)
    print('date: ', update.message.date)
    print('chat: ', vars(update.message.chat))
    print('chat_id: ', vars(update.message.chat_id))
    print('photos list: ', update.message.photo)
    print('stickers: ', update.message.sticker)
    print('video: ', update.message.video)

    print('Full name: ',
          f'{update.message.chat.first_name} '
          f'{update.message.chat.last_name}')

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello i am your updated bot !"
    )


@t.message(ext.Filters.command)
def unknown_msg(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command."
    )


@t.inline
def upper_or_lower(bot, update):
    q = update.inline_query.query

    if not q:
        return

    results = list()
    results.append(
        InlineQueryResultArticle(
            id=q.upper(),
            title='Upper',
            input_message_content=InputTextMessageContent(q.upper())
        )
    )
    results.append(
        InlineQueryResultArticle(
            id=q.lower(),
            title='Lower',
            input_message_content=InputTextMessageContent(q.lower())
        )
    )

    bot.answer_inline_query(update.inline_query.id, results)


@t.job(interval=10, first=0, repeating=True)
def send_hello(bot, job):
    from pprint import pprint

    print('job: ')
    pprint(vars(job))


if __name__ == '__main__':
    t.run()