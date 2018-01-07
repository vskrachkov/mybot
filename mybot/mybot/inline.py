from telegram import InlineQueryResultArticle, InputTextMessageContent

from .bot import bot


@bot.inline
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